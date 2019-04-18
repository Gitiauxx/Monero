#include <boost/iostreams/device/mapped_file.hpp>
#include<vector>
#include<chrono>
#include<iostream>
#include<fstream>
#include<unordered_map>


struct Input {
	std::string tx;
	std::string key;
};

//storing edge as pair (transaction, number of keys in common)
// it may be clumsy but then, we do not need to look at input keys anymore
struct Edge {
    int tx;
    int nk;
};

struct Node {
    public:
        std::vector<Edge> edge;
        int n_tx;
        int n_key;
};

// data folder
std::string DATA = "C:\\Users\\Xavier\\monero\\data\\inputs\\monero_inputs";
std::string KEY = "C:\\Users\\Xavier\\monero\\data\\keys\\keys";

// an unordered  map to map keys to transaction
std::unordered_map<std::string, std::vector<int>> key_register;

int node_id = 0; // store transactions as integer from 0 on...
std::string key5;

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
			data.emplace_back(input); // add value
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
			tx_register.emplace_back(count_key);	
			count_key= 1;	
		}
	}

    // push the last one
    tx_register.emplace_back(count_key);

    // for each transaction, put it on the transaction graph and 
    // add the transaction in the key_register
    int key_start = 0;
    std::string tx;
    int tot_count = 0;
  
    for (std::vector<int>::iterator it = tx_register.begin(); it != tx_register.end(); ++it)
		{
            int count = 0;
            tot_count += *it;

            // fill the key_registery
            
            while (count < *it) 
            {
                tx = data[key_start].tx;
                
                std::string key = data[key_start].key;
                key_register[key].push_back(node_id);
                if (node_id == 5) key5 = key;
            
                count += 1;
                key_start += 1;
    
            }

            
            node_id += 1;
  
		}

    std::cout << data[1999999].tx << '\n';
    std::cout << tx << '\n';
    std::cout << tot_count << '\n';
}

void KeyRegistery(){
    for (int i = 0; i <= 38; i++) 
    {
		std::string inFile = DATA;
		
		// Add the number to the filename
        inFile.append(std::to_string(i));

		// Add the suffix to the filename
        inFile.append(".csv");
		std::cout << "Reading file "<< inFile << std::endl;

        // construct graph for inFile
        ReadFile(inFile);

    }
}

void SaveKeyChunks(int chunk_size, std::string filename){
    std::unordered_map<std::string, std::vector<int>>::iterator key_it = key_register.begin();
    int count_key = 0;

    //open file stream
    std::ofstream outFile(filename);

    while(key_it != key_register.end() && count_key < chunk_size)
    {
        std::vector<int> key_tx = key_it -> second;
        std::vector<int>::iterator tx_it;
        
        for (tx_it = key_tx.begin(); tx_it != key_tx.end(); ++ tx_it)
        {
            outFile << *tx_it << ',';
            if (key_it -> first == key5){
                std::cout << *tx_it << '\n';
            }
        }
        outFile << "\n"; 
        key_it = key_register.erase(key_it);
        count_key += 1;
    }

    outFile.close();
}

void SaveKey(int chunk_size){
    
    int filenumber = 0;
    while (key_register.size() > 0)
    {
		std::string outFile = KEY;
		
		// Add the number to the filename
        outFile.append(std::to_string(filenumber));

		// Add the suffix to the filename
        outFile.append(".csv");
		std::cout << "Writing file "<< outFile << std::endl;

        // construct graph for inFile
        SaveKeyChunks(chunk_size, outFile);
        filenumber += 1;

    }
}

int main()
{
    auto start = std::chrono::high_resolution_clock::now();
    
    KeyRegistery();
    SaveKey(5 * 1000 * 1000);
    
    auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end - start;
	std::cout << elapsed.count() << '\n';
    std::cout << node_id <<'\n';

    return 0;
}
