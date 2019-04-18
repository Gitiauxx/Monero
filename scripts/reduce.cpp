#include <boost/iostreams/device/mapped_file.hpp>
#include<vector>
#include<chrono>
#include<iostream>
#include<unordered_map>
#include<fstream>

std::string GRAPH = "C:\\Users\\Xavier\\monero\\data\\graph\\";

// graph is represented as nodes and adjacent maps of edges
typedef struct Node {
    int n_key; // number of keys in the nodes
    int n_tx; // number of transactions in the nodes
    std::vector<std::pair<int, int>> edge; // edge with weight for number of common keys

    Node()
    {
        n_key = 0; 
        n_tx = 1;
        edge;
    }

} Node;

// graph
std::unordered_map<int, Node> tx_graph;

void graphFile(std::string filename){
    
    boost::iostreams::mapped_file mmap(filename);
    auto chars = mmap.const_data(); // set data to char array
    auto eofile = chars + mmap.size(); 
    std::string next = ""; // used to read in chars
    
    std::vector<std::vector<int> > data;
    std::vector< std::pair<int, int>> edge;

    int flag_edge = 0;
    Node node;
    std::pair<int, int> edge_link;

    int e, ne, tx;

    for (; chars && chars != eofile; chars++)
    {
        
        if (chars[0] != ':' && chars[0] != '\n' && chars[0] != ',' && chars[0] != '{' && chars[0] != '}' && chars[0] != '(' && chars[0] != ')')
        {
            next += chars[0]; // add to read string
        }
        
        else if (chars[0] == ':')
        {
            tx = std::stol(next, nullptr, 10); 
            next = "";
        }

        else if (chars[0] == ',')
        {
            if (flag_edge == 0) 
            {
                flag_edge = 1;
                node.n_key = std::stol(next, nullptr, 10);
                next = "";
            } 
            else if (flag_edge == 2) 
            {
                flag_edge = 1;
                e = std::stol(next, nullptr, 10);
                next = "";
            }
        }

        else if (chars[0] == '(')
        {
                flag_edge = 2;
        }

        else if (chars[0] == ')')
        {
                flag_edge = 1;
                ne = std::stol(next, nullptr, 10);
                next = "";
                edge_link = {e, ne};
                edge.push_back(edge_link);
        }

        else if (chars[0] == '\n')
        {
            if (edge.size() > 0) 
            {
                node.edge = edge;
                tx_graph[tx] = node; 
            } 
            next = "";    
            edge.clear(); 
            flag_edge = 0;
        }
        
    }
}

void reduceGraph(){
    std::unordered_map<int, Node>::iterator it = tx_graph.begin();
    
    while(it != tx_graph.end())
    {
        Node node = it -> second;
        std::vector<std::pair<int, int>> edge = node.edge;
        std::vector<std::pair<int, int>>::iterator edge_it = edge.begin();
        int absorbed = 0;
        
        while(edge_it != edge.end() && absorbed == 0)
        {
            if (edge_it -> second == node.n_key)
            {
                absorbed = 1;
                Node node_abs = tx_graph[edge_it -> first];
                node_abs.n_tx += 1;
                tx_graph[edge_it -> first] =  node_abs;
                
            }
            ++edge_it;
        }

        if (absorbed == 1)
        {
            it = tx_graph.erase(it);
        }
        else
        {
            {
                ++it;
            }
        }
    }

}

int main(){

    std::string filename = GRAPH;
    filename.append("graph_tx.csv");
    graphFile(filename);
    std::cout << tx_graph.size();
    
    reduceGraph();
    std::cout << tx_graph.size();


    
    return 0;
}

