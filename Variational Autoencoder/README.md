Variational Autoencoder (VAE) for MNIST Digits

This project implements a Variational Autoencoder (VAE) using PyTorch to generate and reconstruct handwritten digits from the MNIST dataset.

🚀 Overview

A Variational Autoencoder is a type of generative model that learns to encode input data into a latent space, then decodes samples from this space to generate new data. This project trains a VAE to generate realistic digits after learning their underlying distribution.

📦 Features

Encoder and decoder networks built with fully connected layers.

Reparameterization trick for sampling latent vectors.

Loss function combining binary cross-entropy and KL divergence.

Visualization of reconstructed and generated digits during training.

🏃‍♂️ How to Run

Clone this repository:

git clone https://github.com/M-Eisa/My-Projects.git
cd My-Projects

Install dependencies:

pip install torch torchvision

Train the VAE:

python vae.py

Generated images will be saved in the vae_images folder.

🧠 Model Architecture

Encoder: Maps input data to a latent space (mu and logvar for reparameterization).

Reparameterization trick: Samples latent vectors using z = mu + eps * std.

Decoder: Generates data from sampled latent vectors.

📊 Loss Function

The loss combines:

Reconstruction loss (Binary Cross-Entropy): Measures how well the output matches the input.

KL Divergence: Regularizes the latent space to approximate a standard normal distribution.

BCE = nn.functional.binary_cross_entropy(recon_x, x.view(-1, input_dim), reduction='sum')
KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
loss = BCE + KLD

🏞️ Sample Results

Reconstructed Digits: Saved as vae_images/reconstruction_{epoch}.png

Generated Samples: Saved as vae_images/sample.png

