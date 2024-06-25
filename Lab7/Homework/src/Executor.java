import org.apache.zookeeper.*;
import org.apache.zookeeper.data.Stat;

import javax.swing.*;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Executor implements Watcher {

    private final String mainNode = "/a";

    private final ZooKeeper zk;
    private String externalApp;
    private Process externalProcess;
    private JFrame frame;
    private JLabel label;
    private List<String> tree;

    public static void main(String[] args) throws IOException, InterruptedException, KeeperException {

        String externalApp = args[0];
        Executor executor = new Executor("localhost:2181", externalApp);
        executor.zk.addWatch(executor.mainNode, AddWatchMode.PERSISTENT_RECURSIVE);

        Thread.sleep(Long.MAX_VALUE);
    }


    public Executor(String hostPort, String externalApp) throws IOException {
        this.externalApp = externalApp;
        this.zk = new ZooKeeper(hostPort, 3000, this);

    }

    @Override
    public void process(WatchedEvent watchedEvent) {
        String path = watchedEvent.getPath();
        if (watchedEvent.getType() == Event.EventType.NodeCreated && path.equals(mainNode)) {
            System.out.println("Main noode created");

            try {
                ProcessBuilder pb = new ProcessBuilder();
                pb.command(this.externalApp);
                this.externalProcess = pb.start();
            } catch (IOException e) {
                e.printStackTrace();
            }
            displayOnFrame();

        } else if (watchedEvent.getType() == Event.EventType.NodeCreated && path.startsWith(mainNode)) {
            System.out.println("Element of tree added");
            displayOnFrame();
        } else if (watchedEvent.getType() == Event.EventType.NodeDeleted && path.equals(mainNode)) {
            System.out.println("Main node removed");

            if (this.externalProcess != null) {
                this.externalProcess.destroy();
            }
            if (frame != null) {
                frame.dispose();
            }
            System.exit(0);
        } else if (watchedEvent.getType() == Event.EventType.NodeDeleted && path.startsWith(mainNode)) {
            System.out.println("Element of tree removed");
            displayOnFrame();
        }

    }

    public void displayOnFrame() {
        SwingUtilities.invokeLater(() -> {
            if (frame == null) {
                frame = new JFrame();
                frame.setSize(300, 200);
                frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

                label = new JLabel();
                frame.getContentPane().add(label);
                frame.setVisible(true);
            }

            this.tree = new ArrayList<>();


            int childern = 0;
            try {
                getTreePaths(mainNode);
                childern = countChildern(mainNode) - 1;
            } catch (InterruptedException e) {
                //
            } catch (KeeperException e) {
                //
            }
            TreeBuilder treeBuilder = new TreeBuilder();
            Node root = treeBuilder.buildTree(this.tree);
            String treeString = treeBuilder.buildTreeString(root, "", "");
            label.setText("<html><pre>Childern count: " + childern + "\n" + treeString + "</pre></html>");
        });
    }


    public void getTreePaths(String path) throws InterruptedException, KeeperException {
        List<String> childern = this.zk.getChildren(path, false);

        Stat stat = this.zk.exists(path, false);
        if (stat == null) {
            return;
        }

        if (childern.isEmpty()) {
            this.tree.add(path + "\n");
        }

        for (String child : childern) {
            String newPath = path + "/" + child;
            getTreePaths(newPath);
        }

    }

    public int countChildern(String path) throws InterruptedException, KeeperException {
        int sum = 1;

        Stat stat = this.zk.exists(path, false);
        if (stat == null) {
            return -1;
        }

        List<String> childern = this.zk.getChildren(path, false);
        for (String child : childern) {
            String newPath = path + "/" + child;
            sum += countChildern(newPath);
        }

        return sum;
    }
}