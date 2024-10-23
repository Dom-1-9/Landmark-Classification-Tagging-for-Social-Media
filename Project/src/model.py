import torch
import torch.nn as nn


# define the CNN architecture
class MyModel(nn.Module):
    def __init__(self, num_classes: int = 1000, dropout: float = 0.7) -> None:

        super().__init__()
        
        self.model = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=8, kernel_size=3, padding='same', stride=1),
            nn.BatchNorm2d(8),
            nn.ReLU(),
            nn.Conv2d(8, 16, 3, padding='same', stride=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            
            nn.Conv2d(16, 32, 3, padding='same', stride=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.Conv2d(32, 64, 3, padding='same', stride=1),
            nn.BatchNorm2d(64),
            nn.MaxPool2d(2,2),
            
            nn.Conv2d(64, 128, 3, padding='same', stride=1),
            nn.BatchNorm2d(128),
            nn.ReLU(),
            nn.Conv2d(128, 256, 3, padding='same', stride=1),
            nn.BatchNorm2d(256),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            
            nn.Conv2d(256, 512, 3, padding='same', stride=1),
            nn.BatchNorm2d(512),
            nn.ReLU(),
            nn.MaxPool2d(2,2),
            
            nn.Flatten(),
            
            nn.Linear(512*14*14, 5120),
            nn.BatchNorm1d(5120),
            nn.ReLU(),
            nn.Dropout(dropout),
            
            nn.Linear(5120 , 1024),
            nn.BatchNorm1d(1024),
            nn.ReLU(),
            nn.Dropout(dropout),
            
            nn.Linear(1024, num_classes)
        )

        # YOUR CODE HERE
        # Define a CNN architecture. Remember to use the variable num_classes
        # to size appropriately the output of your classifier, and if you use
        # the Dropout layer, use the variable "dropout" to indicate how much
        # to use (like nn.Dropout(p=dropout))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.model(x)
        # YOUR CODE HERE: process the input tensor through the
        # feature extractor, the pooling and the final linear
        # layers (if appropriate for the architecture chosen)
        return x


######################################################################################
#                                     TESTS
######################################################################################
import pytest


@pytest.fixture(scope="session")
def data_loaders():
    from .data import get_data_loaders

    return get_data_loaders(batch_size=2)


def test_model_construction(data_loaders):

    model = MyModel(num_classes=23, dropout=0.3)

    dataiter = iter(data_loaders["train"])
    images, labels = dataiter.next()

    out = model(images)

    assert isinstance(
        out, torch.Tensor
    ), "The output of the .forward method should be a Tensor of size ([batch_size], [n_classes])"

    assert out.shape == torch.Size(
        [2, 23]
    ), f"Expected an output tensor of size (2, 23), got {out.shape}"