import java.util.*;

class Node {
    String name;
    Map<String, Node> children = new HashMap<>();

    Node(String name) {
        this.name = name;
    }
}

public class TreeBuilder {
    public Node buildTree(List<String> paths) {
        Node root = new Node("");
        for (String path : paths) {
            Node current = root;
            String[] segments = path.split("/");

            for (String segment : segments) {
                if (!segment.isEmpty()) {
                    current = current.children.computeIfAbsent(segment, Node::new);
                }
            }
        }
        return root;
    }

    public String buildTreeString(Node node, String prefix, String childrenPrefix) {
        StringBuilder sb = new StringBuilder();
        List<Node> children = new ArrayList<>(node.children.values());
        for (int i = 0; i < children.size(); i++) {
            Node next = children.get(i);
            boolean isLast = i == children.size() - 1;

            if (isLast) {
                sb.append(childrenPrefix).append("+--").append(next.name).append("\n");
                sb.append(buildTreeString(next, childrenPrefix + "   ", childrenPrefix + "   "));
            } else {
                sb.append(childrenPrefix).append("+--").append(next.name).append("\n");
                sb.append(buildTreeString(next, childrenPrefix + "|  ", childrenPrefix + "|  "));
            }
        }
        return sb.toString();
    }
}
