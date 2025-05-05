# from stable_baselines3 import PPO
# from cinquillo_env import CinquilloEnv  

# env = CinquilloEnv()
# model = PPO("MlpPolicy", env, verbose=1, device="cpu")
# model.learn(total_timesteps=100000)
# model.save("cinquillo_agent")


from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import CheckpointCallback
from cinquillo_env import CinquilloEnv
import torch

if __name__ == "__main__":
    # Crear entorno
    env = DummyVecEnv([lambda: CinquilloEnv()])

    # Detectar dispositivo
    device = "cpu"
    print("Usando dispositivo:", device)

    # Crear modelo PPO
    model = PPO(
        "MlpPolicy",
        env,
        verbose=1,
        device=device,
        tensorboard_log="./logs_tensorboard",
        n_steps=2048,
        batch_size=512,
        learning_rate=3e-4,
        gamma=0.8,
    )

    # Callback para guardar checkpoints
    checkpoint_callback = CheckpointCallback(
        save_freq=10000,  # cada 10k pasos
        save_path="./checkpoints/",
        name_prefix="ppo_cinquillo"
    )

    # Entrenar el modelo
    model.learn(
        total_timesteps=200_000,
        callback=checkpoint_callback
    )

    # Guardar modelo final
    model.save("ppo_cinquillo_final")
    print("\nModelo entrenado y guardado.")