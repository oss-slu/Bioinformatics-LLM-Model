# Hyperparameter Tuning
## Learning Rate

I made a simple finetuning script to tune the learning rate parameter. According to the babysitting methodology, we can test whether a learning rate will lead the training to converge by simple training it over a handful of datapoints. An optimal learning rate should allow the model to converge over the first few epochs. 

# Methods and Results

I constructed a simple training framework that runs for 5 epochs, testing the following learning rates commonly used in finetuning transformer architectures: 1e-5, 5e-5, 1e-4, and 5e-4. It was observed that learning rates of 1e-5 and 5e-5 are too small and will likely prevent the model from converging optimally. On the other hand, a learning rate of 1e-4 proved to be quite unstable. 5e-4 was the most optimal learning rate of the batch and will likely be the learning rate that we can use to further  finetune our model with the final script. 