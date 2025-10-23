import torch
import torch.nn as nn
import numpy as np
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


class TimeSeriesDiffusion(nn.Module):
    """
    Diffusion model for time series forecasting

    This model uses denoising diffusion probabilistic models (DDPM)
    adapted for financial time series prediction.
    """

    def __init__(
        self,
        input_dim=5,
        hidden_dim=128,
        num_layers=4,
        num_timesteps=1000,
        lookback_window=60,
        forecast_horizon=10
    ):
        super().__init__()

        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.num_timesteps = num_timesteps
        self.lookback_window = lookback_window
        self.forecast_horizon = forecast_horizon

        self.betas = self._cosine_beta_schedule(num_timesteps)
        self.alphas = 1.0 - self.betas
        self.alphas_cumprod = torch.cumprod(self.alphas, dim=0)
        self.alphas_cumprod_prev = torch.cat([
            torch.tensor([1.0]),
            self.alphas_cumprod[:-1]
        ])

        self.sqrt_alphas_cumprod = torch.sqrt(self.alphas_cumprod)
        self.sqrt_one_minus_alphas_cumprod = torch.sqrt(1.0 - self.alphas_cumprod)

        self.encoder = self._build_encoder()

        self.denoiser = self._build_denoiser()

        self.condition_encoder = nn.Sequential(
            nn.Linear(lookback_window * input_dim, hidden_dim * 2),
            nn.GELU(),
            nn.LayerNorm(hidden_dim * 2),
            nn.Linear(hidden_dim * 2, hidden_dim),
            nn.GELU()
        )

        logger.info(f'TimeSeriesDiffusion initialized: lookback={lookback_window}, horizon={forecast_horizon}')

    def _build_encoder(self):
        """Build the temporal encoder network"""
        layers = []

        layers.append(nn.Linear(self.input_dim + 1, self.hidden_dim))
        layers.append(nn.GELU())
        layers.append(nn.LayerNorm(self.hidden_dim))

        for _ in range(self.num_layers):
            layers.append(nn.Linear(self.hidden_dim, self.hidden_dim))
            layers.append(nn.GELU())
            layers.append(nn.LayerNorm(self.hidden_dim))
            layers.append(nn.Dropout(0.1))

        return nn.Sequential(*layers)

    def _build_denoiser(self):
        """Build the denoising network"""
        return nn.Sequential(
            nn.Linear(self.hidden_dim, self.hidden_dim * 2),
            nn.GELU(),
            nn.LayerNorm(self.hidden_dim * 2),
            nn.Dropout(0.1),
            nn.Linear(self.hidden_dim * 2, self.hidden_dim),
            nn.GELU(),
            nn.LayerNorm(self.hidden_dim),
            nn.Linear(self.hidden_dim, self.forecast_horizon * self.input_dim)
        )

    def _cosine_beta_schedule(self, timesteps, s=0.008):
        """Cosine schedule for beta values (more stable than linear)"""
        steps = timesteps + 1
        x = torch.linspace(0, timesteps, steps)
        alphas_cumprod = torch.cos(((x / timesteps) + s) / (1 + s) * torch.pi * 0.5) ** 2
        alphas_cumprod = alphas_cumprod / alphas_cumprod[0]
        betas = 1 - (alphas_cumprod[1:] / alphas_cumprod[:-1])
        return torch.clip(betas, 0.0001, 0.9999)

    def forward(self, x, t, condition):
        """
        Forward pass through the diffusion model

        Args:
            x: Noisy forecast [batch, forecast_horizon, input_dim]
            t: Timestep [batch]
            condition: Historical data [batch, lookback_window, input_dim]

        Returns:
            Predicted noise
        """
        batch_size = x.shape[0]

        condition_flat = condition.reshape(batch_size, -1)
        condition_embedding = self.condition_encoder(condition_flat)

        t_embedding = self._get_timestep_embedding(t, self.hidden_dim)

        x_flat = x.reshape(batch_size, -1)
        x_with_t = torch.cat([x_flat, t_embedding], dim=-1)

        encoded = self.encoder(x_with_t)

        combined = encoded + condition_embedding

        noise_pred = self.denoiser(combined)

        noise_pred = noise_pred.reshape(batch_size, self.forecast_horizon, self.input_dim)

        return noise_pred

    def _get_timestep_embedding(self, timesteps, embedding_dim):
        """Sinusoidal timestep embeddings"""
        half_dim = embedding_dim // 2
        embeddings = torch.log(torch.tensor(10000.0)) / (half_dim - 1)
        embeddings = torch.exp(torch.arange(half_dim) * -embeddings)
        embeddings = timesteps[:, None] * embeddings[None, :]
        embeddings = torch.cat([torch.sin(embeddings), torch.cos(embeddings)], dim=-1)

        if embedding_dim % 2 == 1:
            embeddings = torch.nn.functional.pad(embeddings, (0, 1))

        return embeddings

    def q_sample(self, x_start, t, noise=None):
        """
        Forward diffusion process: add noise to data

        Args:
            x_start: Clean data
            t: Timestep
            noise: Optional noise to add

        Returns:
            Noisy data
        """
        if noise is None:
            noise = torch.randn_like(x_start)

        sqrt_alphas_cumprod_t = self.sqrt_alphas_cumprod[t]
        sqrt_one_minus_alphas_cumprod_t = self.sqrt_one_minus_alphas_cumprod[t]

        while len(sqrt_alphas_cumprod_t.shape) < len(x_start.shape):
            sqrt_alphas_cumprod_t = sqrt_alphas_cumprod_t.unsqueeze(-1)
            sqrt_one_minus_alphas_cumprod_t = sqrt_one_minus_alphas_cumprod_t.unsqueeze(-1)

        return sqrt_alphas_cumprod_t * x_start + sqrt_one_minus_alphas_cumprod_t * noise

    def p_sample(self, x, t, condition):
        """
        Reverse diffusion process: denoise data one step

        Args:
            x: Noisy data
            t: Current timestep
            condition: Conditioning information

        Returns:
            Slightly less noisy data
        """
        batch_size = x.shape[0]

        noise_pred = self.forward(x, t, condition)

        beta_t = self.betas[t]
        sqrt_one_minus_alphas_cumprod_t = self.sqrt_one_minus_alphas_cumprod[t]
        sqrt_recip_alphas_t = torch.sqrt(1.0 / self.alphas[t])

        while len(beta_t.shape) < len(x.shape):
            beta_t = beta_t.unsqueeze(-1)
            sqrt_one_minus_alphas_cumprod_t = sqrt_one_minus_alphas_cumprod_t.unsqueeze(-1)
            sqrt_recip_alphas_t = sqrt_recip_alphas_t.unsqueeze(-1)

        model_mean = sqrt_recip_alphas_t * (
            x - beta_t * noise_pred / sqrt_one_minus_alphas_cumprod_t
        )

        if t[0] == 0:
            return model_mean
        else:
            noise = torch.randn_like(x)
            posterior_variance_t = self.betas[t]
            while len(posterior_variance_t.shape) < len(x.shape):
                posterior_variance_t = posterior_variance_t.unsqueeze(-1)
            return model_mean + torch.sqrt(posterior_variance_t) * noise

    @torch.no_grad()
    def p_sample_loop(self, condition, shape):
        """
        Full reverse diffusion process: generate forecast

        Args:
            condition: Historical data for conditioning
            shape: Shape of output to generate

        Returns:
            Generated forecast
        """
        device = next(self.parameters()).device
        batch_size = shape[0]

        x = torch.randn(shape).to(device)

        for i in reversed(range(self.num_timesteps)):
            t = torch.full((batch_size,), i, dtype=torch.long).to(device)
            x = self.p_sample(x, t, condition)

        return x

    def compute_loss(self, x_start, condition):
        """
        Compute training loss

        Args:
            x_start: Ground truth future data
            condition: Historical data

        Returns:
            Loss value
        """
        batch_size = x_start.shape[0]
        device = x_start.device

        t = torch.randint(0, self.num_timesteps, (batch_size,)).to(device)

        noise = torch.randn_like(x_start)

        x_noisy = self.q_sample(x_start, t, noise)

        noise_pred = self.forward(x_noisy, t, condition)

        loss = nn.functional.mse_loss(noise_pred, noise)

        return loss
