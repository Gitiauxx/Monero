#include <boost/iostreams/device/mapped_file.hpp>
#include<vector>
#include<chrono>
#include<iostream>
#include<unordered_map>


struct Input {
	std::string tx;
	std::string key;
};

struct Node {
    public:
        std::vector<std::string> edge;
        int n_tx;
        int n_key;

        //constructor
        //Node(int n_tx, int n_key): 
            //n_tx(n_tx), n_key(n_key)
        //{}
};

// data folder
std::string DATA = "C:\\Users\\Xavier\\monero\\data\\inputs\\monero_inputs";

// an unordered  map to map keys to transaction
std::unordered_map<std::string, std::vector<std::string>> key_register;

// unordered map to represent graph
std::unordered_map<std::string, struct Node> tx_graph;

void ReadFile(std::string const& pathname){
    boost::iostreams::mapped_file mmap(pathname);
    
    auto chars = mmap.const_data(); // set data to char array
    auto eofile = chars + mmap.size(); // used to detect end of file
    std::string next = ""; // used to read in chars
    std::vector<Input> data; // store the data
    data.reserve(2 * 1000 * 1000);
    Input input;

    int col= 0;
    int header =0;

    for (; chars && chars != eofile; chars++) {
        if (chars[0] == ',' && col < 4)
		{
            col += 1;
		}

        else if (chars[0] == ',' && col == 4 && header > 0) 
        {
            input.tx = next;
            next = "";
			col += 1;
        }

		else if (chars[0] == ',' && col == 7 && header > 0) 
        {
            input.key = next;
			data.push_back(input); // add value
            next = "";
			col = 0;
			header += 1;
        }

		else if (chars[0] == ',')
        {
            col += 1;
        }

		else  if (col == 4 || col == 7)
            next += chars[0]; // add to read string
            
        else if (chars[0] == '\n')
        {
            next="";
            col=0;
            header += 1;
        } 
    }

    // number of keys per transaction
	std::vector<int> tx_register;
	int count_key = 0;
	std::string tx_name;

	for (std::vector<Input>::iterator it = data.begin(); it != data.end(); ++it) 
	{
		if (count_key == 0)
		{
			tx_name= it->tx;
		}
		
		if ((it -> tx) == tx_name) 
		{
			count_key += 1;
		}
		else
		{
			tx_name = it->tx;
			tx_register.push_back(count_key);	
			count_key= 1;	
		}
	}

    // for each transaction, put it on the transaction graph and 
    // add the transaction in the key_register
    int full = 1;
    int key_start = 0;
    std::string tx;

    for (std::vector<int>::iterator it = tx_register.begin(); it != tx_register.end(); ++it)
		{
            int count = 0;
            std::unordered_map<std::string, int> neighbors;

            while (count < *it) 
            {
                tx = data[key_start].tx;
                //std::cout << key_start << std::endl;
                
                std::string key = data[key_start].key;

                if (key_register.find(key) != key_register.end())
                {
                    std::vector<std::string> temp_neigh = key_register[key];
                
                    // add new potential neighbhors and count the number of times they appear
                    for(std::vector<std::string>::iterator neigh_tx = temp_neigh.begin(); neigh_tx != temp_neigh.end(); ++neigh_tx)
                    {
                        if (neighbors.find(*neigh_tx) != neighbors.end())
                        {
                            neighbors[*neigh_tx] = 1;
                        }
                        else
                        {
                            neighbors[*neigh_tx] +=1;
                        }
                    }
                    // add transaction in key registry
                    key_register[key].push_back(tx);
                }
                else
                {
                    key_register[key] = std::vector<std::string> {tx};
                    full = 0;
                }
                
                count += 1;
                key_start += 1;
            }

            // register transaction into graoh if not included fully in another one
            if (full == 0) 
            {
                std::vector<std::string> edge;
                int n_tx = 1;
                for(std::unordered_map<std::string, int>::iterator neigh_tx = neighbors.begin(); neigh_tx != neighbors.end(); ++neigh_tx)
                {
                    if (tx_graph.find(neigh_tx -> first) != tx_graph.end())
                    {
                        struct Node transaction = tx_graph[(neigh_tx -> first)];
                        if ((neigh_tx -> second) >= transaction.n_key)
                        {
                            tx_graph.erase(neigh_tx -> first);
                            n_tx += 1;
                        }
                        else
                        {
                            edge.push_back((neigh_tx -> first));
                        }
                    }              
                }
                if(edge.size() > 0 && key_start < 1000) 
                {
                    std::cout << key_start << std::endl;
                    std::cout << tx << std::endl;
                    std::cout << edge[0]<< std::endl;
        
                }
                struct Node node = {edge, count, n_tx}; 
                tx_graph[tx] = node;
            }
            else
            {
                std::unordered_map<std::string, int>::iterator neigh_tx = neighbors.begin();
                while (neigh_tx != neighbors.end() && full == 1)
                {
                    if (neigh_tx -> second >= count)
                    {
                        struct Node transaction = tx_graph[(neigh_tx -> first)];
                        transaction.n_tx += 1;
                        tx_graph[neigh_tx -> first] = transaction;
                        full = 0;
                    }
                ++neigh_tx;
                }
            }

            // set value to next transaction
            full = 1;	
        
		}
}


int main()
{
    std::string pathname = "C:\\Users\\Xavier\\monero\\data\\inputs\\monero_inputs0.csv";
    ReadFile(pathname);
    std::cout << tx_graph["943fa8c139b213a6ba4975f9f9dce4efda4af070ac4dd8f783d886afd199bbc0"].n_tx << std::endl;
    return 0;
}
