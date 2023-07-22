import torch
import networkx as nx
from torch import Tensor
from torch_geometric.nn import GCNConv
from torch_geometric.datasets import Planetoid
# Define the graph
G = nx.Graph()
G.add_edges_from([(0, 1, {'weight': 2}), (0, 2, {'weight': 5}),
                  (1, 2, {'weight': 3}), (2, 3, {'weight': 4}),
                  (2, 4, {'weight': 5}), (3, 4, {'weight': 3}),
                  (3, 1, {'weight': 6}), (4, 1, {'weight': 1}),
                  (4, 0, {'weight': 2}), (3, 0, {'weight': 4})])

# Convert the graph to a PyTorch tensor
edge_index = torch.tensor(list(G.edges)).t().contiguous()
edge_weight = torch.tensor([G[u][v]['weight'] for u, v in G.edges], dtype=torch.float)
data = torch_geometric.data.Data(edge_index=edge_index, edge_attr=edge_weight)

# Define the model architecture
class GCN(torch.nn.Module):
    def __init__(self):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(5, 16)
        self.conv2 = GCNConv(16, 1)

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

# Define the loss function
def loss_function(output, target):
    return torch.mean((output - target)**2)

# Define the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Set the target output for vertex 2
target_output = torch.zeros(5)
target_output[2] = 1

# Train the model to minimize the total edge weight
for i in range(1000):
    optimizer.zero_grad()
    output = model(data.edge_attr, data.edge_index)
    loss = loss_function(output, target_output)
    loss += torch.sum(data.edge_attr)
    loss.backward()
    optimizer.step()

# Find the optimal set of edges
edge_mask = (torch.sigmoid(model.conv2.weight) > 0.5).squeeze()
