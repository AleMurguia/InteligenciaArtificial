import java.util.*;

public class EightPuzzle {
    private int maxFrontierSize = 0;

    public static void main(String[] args) {
        EightPuzzle puzzleSolver = new EightPuzzle();
        Scanner inputScanner = new Scanner(System.in);
        String hearts = "♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥ ♥";
        String startState;

        System.out.println(hearts);
        System.out.println("Choose the start state:");
        System.out.println("1. 013425678");
        System.out.println("2. 867254301");
        System.out.println("3. 876543210");
        System.out.println(hearts);

        int startStateChoice = inputScanner.nextInt();

        // Asignación del estado inicial basado en la respuesta del usuario.
        switch (startStateChoice) {
            case 1:
                startState = "013425678";
                break;
            case 2:
                startState = "867254301";
                break;
            case 3:
                startState = "876543210";
                break;
            default:
                System.out.println("Invalid. Please enter 1, 2, or 3.");
                inputScanner.close();
                return;
        }

        System.out.println(hearts);
        System.out.println("Choose one kind of search: ");
        System.out.println("1.- Breadth First Search");
        System.out.println("2.- Depth First Search");
        System.out.println(hearts);

        int searchOption = inputScanner.nextInt();
        String searchType;
        long startTime = System.currentTimeMillis();
        long elapsedTime;

        // Ejecución del tipo de búsqueda elegido.
        switch (searchOption) {
            case 1:
                searchType = "Breadth First Search";
                puzzleSolver.breadthFirstSearch(startState);
                break;
            case 2:
                searchType = "Depth First Search";
                puzzleSolver.depthFirstSearch(startState);
                break;
            default:
                System.out.println("Invalid option");
                return;
        }

        // Cálculo del tiempo y espacio transcurrido.
        elapsedTime = System.currentTimeMillis() - startTime;
        System.out.println(searchType);
        System.out.println("Time: " + elapsedTime + " milliseconds");
        System.out.println("Space: " + puzzleSolver.maxFrontierSize + " nodes");

        inputScanner.close();
    }


    //Expande el nodo actual, genera y agrega sus sucesores no explorados,
    //muestra la solución si se alcanza el estado objetivo.
    private boolean expandNode(Node currentNode, Collection<Node> frontier, Set<String> exploredStates) {
        if (isGoalState(currentNode.state)) {
            displaySolutionPath(currentNode);
            return true;
        }
        exploredStates.add(currentNode.state);
        List<String> childStates = generateSuccessors(currentNode.state);
        for (String child : childStates) {
            if (!exploredStates.contains(child)) {
                Node childNode = new Node(child, currentNode);
                frontier.add(childNode);
            }
        }
        return false;
    }


    // Implementación de la búsqueda en anchura (BFS).
    public void breadthFirstSearch(String startState) {
        Queue<Node> frontier = new LinkedList<>();
        Set<String> exploredStates = new HashSet<>();
        maxFrontierSize = 0;

        Node rootNode = new Node(startState, null);
        frontier.add(rootNode);

        while (!frontier.isEmpty()) {
            Node currentNode = frontier.poll();
            if (expandNode(currentNode, frontier, exploredStates)) {
                return;
            }
            maxFrontierSize = Math.max(maxFrontierSize, frontier.size());
        }
        System.out.println("No solution found");
    }

    // Implementa la búsqueda en profundidad (DFS)
    public void depthFirstSearch(String startState) {
        Stack<Node> frontier = new Stack<>();
        Set<String> exploredStates = new HashSet<>();
        maxFrontierSize = 0;

        Node rootNode = new Node(startState, null);
        frontier.push(rootNode);

        while (!frontier.isEmpty()) {
            Node currentNode = frontier.pop();
            if (expandNode(currentNode, frontier, exploredStates)) {
                return;
            }
            maxFrontierSize = Math.max(maxFrontierSize, frontier.size());
        }
        System.out.println("No solution found");
    }

    // Genera los sucesores del estado actual basado en los movimientos posibles.
    private List<String> generateSuccessors(String state) {
        List<String> successors = new ArrayList<>();
        int blankIndex = state.indexOf('0');
        int[] moves = {-1, 1, -3, 3}; // Define los movimientos posibles

        for (int move : moves) {
            int newIndex = blankIndex + move;
            if (isValidMove(blankIndex, newIndex)) {
                StringBuilder newState = new StringBuilder(state);
                newState.setCharAt(blankIndex, newState.charAt(newIndex));
                newState.setCharAt(newIndex, '0');
                successors.add(newState.toString());
            }
        }
        return successors;
    }

    private boolean isValidMove(int blankIndex, int newIndex) {
        return newIndex >= 0 && newIndex < 9 &&
                !(blankIndex % 3 == 0 && newIndex % 3 == 2) &&
                !(blankIndex % 3 == 2 && newIndex % 3 == 0);
    }

    // Verifica si el estado actual es el estado objetivo.
    private boolean isGoalState(String state) {
        return "012345678".equals(state);
    }


    // Muestra el camino de solución desde el estado inicial al estado objetivo.
    private void displaySolutionPath(Node goalNode) {
        Stack<String> solutionPath = new Stack<>();
        for (Node node = goalNode; node != null; node = node.parent) {
            solutionPath.push(node.state);
        }

        while (!solutionPath.isEmpty()) {
            System.out.println(formatState(solutionPath.pop()));
        }
    }

    private String formatState(String state) {
        StringBuilder formattedState = new StringBuilder();
        formattedState.append("♥ ♥ ♥ ♥ ♥\n");

        for (int i = 0; i < state.length(); i++) {
            if (i % 3 == 0) formattedState.append("♥ ");

            char tile = state.charAt(i) == '0' ? '-' : state.charAt(i);
            formattedState.append(tile).append(" ");

            if ((i + 1) % 3 == 0) formattedState.append("♥\n");
        }

        formattedState.append("♥ ♥ ♥ ♥ ♥\n");
        return formattedState.toString();
    }

}
