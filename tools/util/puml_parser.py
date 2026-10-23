#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 11:35:43 2026
"""

import re
from dataclasses import dataclass
from typing import Any, Dict, List

import networkx as nx


@dataclass(frozen=True)
class NodeData:
    node_type: str
    name: str
    alias: str


@dataclass(frozen=True)
class EdgeData:
    edge_type: str
    name: str


class PUMLImporter:
    def __init__(self):
        self.graph = nx.DiGraph()

    def parse(self, puml_text: str) -> nx.DiGraph:
        """
        Parses PUML text and populates the networkx graph.
        """
        # Regex Patterns
        # Matches: entity "Real Name" as alias { content }
        entity_block_pattern = re.compile(
            r'entity\s+"([^"]+)"\s+as\s+(\w+)\s*\{([^}]+)\}', re.DOTALL
        )
        # Matches: * id : str (PK) or id : str
        attribute_pattern = re.compile(
            r"[*+]?\s*(\w+)\s*:\s*([^(\n]+)(?:\s*\(([^)]+)\))?"
        )
        # Matches: alias1 ||--o{ alias2 : "relation_name"
        relationship_pattern = re.compile(r'(\w+)\s+(\S+)\s+(\w+)\s*:\s*"([^"]+)"')

        # 1. Parse Entity Blocks
        for block_match in entity_block_pattern.finditer(puml_text):
            real_name, alias, content = block_match.groups()

            # Add Entity Node
            self.graph.add_node(
                alias,
                **NodeData(node_type="entity", name=real_name, alias=alias).__dict__,
            )

            # Parse contents of the entity block
            for line in content.strip().split("\n"):
                line = line.strip()
                if not line:
                    continue

                # Handle Separator (e.g., --)
                if line == "--":
                    sep_id = f"{alias}_separator_{hash(line)}"
                    self.graph.add_node(
                        sep_id,
                        **NodeData(node_type="separator", name="--", alias="").__dict__,
                    )
                    self.graph.add_edge(
                        alias,
                        sep_id,
                        **EdgeData(edge_type="has attribute", name="").__dict__,
                    )

                # Handle Attribute
                elif ":" in line:
                    attr_match = attribute_pattern.search(line)
                    if attr_match:
                        attr_name, attr_type_raw, attr_constraint = attr_match.groups()

                        # Clean up alias (combine type and constraint if present)
                        attr_alias = attr_type_raw.strip()
                        if attr_constraint:
                            attr_alias += f" ({attr_constraint.strip()})"

                        attr_id = f"{alias}_{attr_name}"
                        self.graph.add_node(
                            attr_id,
                            **NodeData(
                                node_type="attribute", name=attr_name, alias=attr_alias
                            ).__dict__,
                        )
                        # Edge from Entity to Attribute
                        self.graph.add_edge(
                            alias,
                            attr_id,
                            **EdgeData(edge_type="has attribute", name="").__dict__,
                        )

        # 2. Parse Relationships (outside entity blocks)
        for rel_match in relationship_pattern.finditer(puml_text):
            src, symbol, tgt, rel_name = rel_match.groups()
            # Only create edge if both nodes exist (prevents orphan relationships)
            if self.graph.has_node(src) and self.graph.has_node(tgt):
                self.graph.add_edge(
                    src, tgt, **EdgeData(edge_type=symbol, name=rel_name).__dict__
                )

        return self.graph

    def to_schema_tree(self) -> List[Dict[str, Any]]:
        """
        Converts the graph into a hierarchical list/dict tree.
        The resulting structure is optimized for Jinja2 templates.
        """
        schema_tree = []

        # We only iterate over nodes that are 'entities'
        entity_nodes = [
            n for n, d in self.graph.nodes(data=True) if d.get("node_type") == "entity"
        ]

        for node_id in entity_nodes:
            node_data = self.graph.nodes[node_id]
            entity_info = {
                "name": node_data["name"],
                "alias": node_data["alias"],
                "attributes": [],
                "relations": [],
            }

            # Traverse neighbors to find attributes and relationships
            for neighbor in self.graph.neighbors(node_id):
                edge_data = self.graph.get_edge_data(node_id, neighbor)
                # If multiple edges existed, get_edge_data might return a dict;
                # for DiGraph, it returns the attribute dict directly.
                if isinstance(edge_data, dict) and "edge_type" not in edge_data:
                    edge_data = list(edge_data.values())[0]

                if edge_data["edge_type"] == "has attribute":
                    neighbor_data = self.graph.nodes[neighbor]
                    # Only add if it's actually an attribute (skip separators)
                    if neighbor_data.get("node_type") == "attribute":
                        entity_info["attributes"].append(
                            {
                                "name": neighbor_data["name"],
                                "type": neighbor_data["alias"],
                            }
                        )
                else:
                    # It is a relationship edge
                    target_data = self.graph.nodes[neighbor]
                    entity_info["relations"].append(
                        {
                            "target_name": target_data["name"],
                            "target_alias": target_data["alias"],
                            "type": edge_data["edge_type"],
                            "name": edge_data["name"],
                        }
                    )

            schema_tree.append(entity_info)

        return schema_tree


# --- Example Usage ---
if __name__ == "__main__":
    puml_content = """
@startuml
entity "person" as person {
  * id : str (PK)
  --
  email : str
  name : str
}

entity "project" as project {
  * id : int (PK)
  --
  key : str (unique)
  name : str
  description : text
  archived : bool
  assignee_type : str
  type_key : str
  lead_id : str (FK)
}

entity "issue" as issue {
  * id : int (PK)
  --
  key : str (unique)
  assignee_id : str (FK)
  creator_id : str (FK)
  reporter_id : str (FK)
  issue_type_id : int (FK)
  priority_id : int (FK)
  project_id : int (FK)
  resolution_id : int (FK)
  status_id : int (FK)
  created_date : datetime
  due_date : datetime
  resolution_date : datetime
  summary : str
  description : text
}

entity "issuelink" as issuelink {
  * id : int (PK)
  --
  type_id : int (FK)
  inward_issue_id : int (FK)
  outward_issue_id : int (FK)
}

person ||--o{ issue : "assignee"
person ||--o{ project : "lead"
project ||--o{ issue : "project"
issue ||--o{ issuelink : "inward"
@enduml
"""

    importer = PUMLImporter()
    importer.parse(puml_content)
    schema = importer.to_schema_tree()

    # Output the result
    import json

    print(json.dumps(schema, indent=2))
