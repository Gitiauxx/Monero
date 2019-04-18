#include <boost/iostreams/device/mapped_file.hpp>
#include<vector>
#include<chrono>
#include<iostream>
#include<unordered_map>
#include<fstream>

std::string DATA = "C:\\Users\\Xavier\\monero\\data\\keys\\keys";
std::string GRAPH = "C:\\Users\\Xavier\\monero\\data\\graph\\";


// graph is represented as nodes and adjacent maps of edges
typedef struct Node {
    int n_key; // number of keys in the nodes
    int n_tx; // number of transactions in the nodes
    std::vector<int> edge; // edge with weight for number of common keys

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
    std::cout << data.size() << '\n';
    //data.reserve(2 * 1000 * 1000 );
    std::vector<int> edge;

    for (; chars && chars != eofile; chars++)
    {
        
        
        if (chars[0] != ',' && chars[0] != '\n')
        {
            next += chars[0]; // add to read string
        }
        
        else if (chars[0] == ',')
        {
            int tx = std::stol(next, nullptr, 10);
            edge.push_back(tx);     
            next = "";
        }

        else if (chars[0] == '\n')
        {
            data.push_back(edge); 
            next = "";    
            edge.clear();  
        }
        
    }

    std::cout << data.size() << '\n';

    std::vector<std::vector<int>>::iterator data_it;
    for (data_it = data.begin(); data_it != data.end(); ++data_it)
    {
        
        std::vector<int>::iterator tx_it1;
        std::vector<int>::iterator tx_it2;
        std::vector<int> temp_edge;
       

        for(tx_it1 = (*data_it).begin(); tx_it1 != (*data_it).end(); ++ tx_it1)
        {

            Node node1 = tx_graph[*tx_it1];
            //Node* node1 = new Node;
            node1.n_key += 1;
            
            //tx_graph.push_back(*data_it);

            for(tx_it2 = (*data_it).begin(); tx_it2 != (*data_it).end(); ++ tx_it2)
            {
                if (*tx_it1 != *tx_it2)
                {
                    temp_edge.push_back(*tx_it2);
               }
                
            }
           
            node1.edge = temp_edge;
            temp_edge.clear();
            tx_graph[*tx_it1] = node1;
        }
        
    }
    
}

void CreateGraph(){
    for (int i = 0; i <= 5; i++) 
    {
		std::string inFile = DATA;
		
		// Add the number to the filename
        inFile.append(std::to_string(i));

		// Add the suffix to the filename
        inFile.append(".csv");
		std::cout << "Reading file "<< inFile << std::endl;

        // construct graph for inFile
        graphFile(inFile);

    }
}

void WriteGraphChunk(std::string filename){
    std::unordered_map<int, Node>::iterator tx_it = tx_graph.begin();
    int count_key = 0;

    //open file stream
    std::ofstream outFile(filename);
    std::cout<<filename << '\n';
    std::unordered_map <int, int> temp_edge;

    while(tx_it != tx_graph.end())
    {
        outFile << tx_it -> first << ':';
        Node node = tx_it -> second;
        outFile << node.n_key << ',';

        // writing edge as a map (int, number of common keys)
        outFile << "{"; 
        std::vector<int>::iterator edge_it;
        
        for (edge_it = node.edge.begin(); edge_it != node.edge.end(); ++edge_it)
        {
            temp_edge[*edge_it] += 1;
        }
        
        std::unordered_map<int, int>::iterator map_it;
        for (map_it = temp_edge.begin(); map_it != temp_edge.end(); ++map_it)
        {
            outFile << "(";
            outFile << map_it -> first << "," << map_it -> second;
            outFile << "),";
        } 
        outFile << "}"; 
        outFile << "\n";
        tx_it = tx_graph.erase(tx_it);
        temp_edge.clear();
        //count_key += 1;
    }

    outFile.close();
}

int main(){
    
    //tx_graph.reserve( 25 * 1000 * 1000);
    CreateGraph();

    std::string filename = GRAPH;
    filename.append("graph_tx.csv");
    WriteGraphChunk(filename);

    return 0;
}