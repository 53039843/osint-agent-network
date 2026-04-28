import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import os
from typing import List, Dict, Any
from utils.logger import setup_logger

logger = setup_logger("graph_utils")

def build_threat_graph(verified_intelligence: List[Dict[str, Any]], target: str) -> nx.DiGraph:
    """
    Builds a directed graph representing relationships between
    threat actors, IoCs, and data sources.
    """
    G = nx.DiGraph()
    
    # Add central target node
    G.add_node(target, type="target", color="red")
    
    for item in verified_intelligence:
        source_node = item.get("source", "unknown")
        ioc_node = f"IoC_{item.get('id', 'unknown')}"
        
        # Add nodes
        G.add_node(source_node, type="source", color="blue")
        G.add_node(ioc_node, type="ioc", color="orange")
        
        # Add edges
        G.add_edge(source_node, ioc_node, label="contains")
        G.add_edge(ioc_node, target, label="related_to")
        
    return G

def export_graph_png(G: nx.DiGraph, target: str, output_dir: str = "reports") -> str:
    """
    Exports the threat graph as a PNG image.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(14, 10))
    
    # Node colors based on type
    color_map = []
    for node in G.nodes(data=True):
        node_type = node[1].get("type", "unknown")
        if node_type == "target":
            color_map.append("red")
        elif node_type == "source":
            color_map.append("steelblue")
        else:
            color_map.append("orange")
    
    pos = nx.spring_layout(G, k=2, seed=42)
    nx.draw_networkx(G, pos, node_color=color_map, with_labels=True, 
                     node_size=1500, font_size=8, arrows=True, 
                     edge_color="gray", alpha=0.9)
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)
    
    plt.title(f"Threat Intelligence Graph: {target}", fontsize=14, fontweight="bold")
    plt.axis("off")
    
    output_path = os.path.join(output_dir, f"threat_graph_{target.replace(' ', '_')}.png")
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    
    logger.info(f"Threat graph saved to {output_path}")
    return output_path
