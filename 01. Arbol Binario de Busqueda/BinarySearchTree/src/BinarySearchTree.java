import javax.swing.*;
public class BinarySearchTree {
    Node root; // Raíz del BST.

    public BinarySearchTree() {
        root = null;
    }

    public void insert(int value) {
        root = insertRecursive(root, value);
    }

    // Actúa para insertar un valor en el lugar correcto del árbol.
    private Node insertRecursive(Node node, int value) {
        if (node == null) {
            node = new Node(value);
            return node;
        }
        if (value < node.value) {
            node.left = insertRecursive(node.left, value);
        }
        else if (value > node.value) {
            node.right = insertRecursive(node.right, value);
        }
        return node;
    }

    // Iniciar el recorrido INORDEN del árbol.
    public String inorder() {
        StringBuilder sb = new StringBuilder();
        inorderRecursive(root, sb);
        if (!sb.isEmpty()){
            sb.setLength(sb.length() - 2);
        }
        return sb.toString().trim();
    }

    // Actúa para realizar el recorrido INORDEN y construir la cadena de salida.
    private void inorderRecursive(Node node, StringBuilder sb) {
        if (node != null) {
            inorderRecursive(node.left, sb);
            sb.append(node.value).append(" - ");
            inorderRecursive(node.right, sb);
        }
    }

    public boolean isEmpty() {
        return root == null;
    }

    public static class TreeUI {
        private final BinarySearchTree tree;

        public TreeUI(BinarySearchTree tree) {
            this.tree = tree;
        }

        // Mostrar el estado del árbol (vacío o su recorrido INORDEN).
        public void display() {
            if (tree.isEmpty()) {
                JOptionPane.showMessageDialog(null, "The tree is empty");
            } else {
                JOptionPane.showMessageDialog(null, "Traversal:\n" + tree.inorder());
            }
        }
    }

    public static void main(String[] args) {
        BinarySearchTree tree = new BinarySearchTree();

        // Insertar valores en el árbol.
        tree.insert(10);
        tree.insert(15);
        tree.insert(5);
        tree.insert(9);
        tree.insert(20);
        tree.insert(30);
        tree.insert(8);
        tree.insert(2);
        tree.insert(3);

        TreeUI ui = new TreeUI(tree);
        ui.display();
    }
}