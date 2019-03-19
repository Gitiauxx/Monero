#include <boost/iostreams/device/mapped_file.hpp>
#include <boost/filesystem.hpp>
#include <boost/thread/thread.hpp>
#include <boost/lockfree/queue.hpp>
#include<vector>
#include<chrono>
#include<iostream>
#include<unordered_map>

struct Input {
	std::string tx;
	std::string key;
};


// hash table to register real-spent key
std::unordered_map<std::string, int> matched;

// number of inputs
int TOTAL_INPUTS = 0;

// data folder
std::string DATA = "C:\\Users\\Xavier\\monero\\data\\inputs\\monero_inputs";


void readCount(std::string const& pathname)
{
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

	TOTAL_INPUTS += data.size();

    // number of keys per transaction
	std::vector<int> transactions;
	int count = 0;
	std::string tx;

	for (std::vector<Input>::iterator it = data.begin(); it != data.end(); ++it) 
	{
		if (count == 0)
		{
			tx = it->tx;
		}
		
		if ((it -> tx) == tx) 
		{
			count += 1;
		}
		else
		{
			tx = it->tx;
			transactions.push_back(count);	
			count = 1;	
		}
	}

	// now launch the cascade attack
	// Iterate over transaction and look up keys for each of them
	int count_mixins = 0;
	std::string key_identified;
	int number_identified = 0;

	while (matched.size() > number_identified || matched.empty())
	{
		number_identified = matched.size();
		int key_start = 0;
		
		for (std::vector<int>::iterator it = transactions.begin(); it != transactions.end(); ++it)
		{
			int key_index = 0;
			
			while (key_index < *it && count_mixins < 2) // if there is 2 or more potential mixins, we can skip this transaction for now
			{
				std::string key;
				key = data[key_start + key_index].key;

				
				// if a key is not in matched, then it has not been idenfied as real spent
				if (matched.find(key) == matched.end())
				{
					count_mixins += 1;
					key_identified = key;
				}

				key_index += 1;

			}

			// within a transaction look for key already matched
			if (count_mixins == 1)
			{
				matched[key_identified] = 1;
			}
			key_start += *it;
			count_mixins = 0;
		}
	}
	
     
}

void cascade()
{
	for (int i = 0; i <= 28; i++) {

		std::string inFile = DATA;
		
		// Add the number to the filename
        inFile.append(std::to_string(i));

		// Add the suffix to the filename
        inFile.append(".csv");
		std::cout << "Reading file "<< inFile << std::endl;

		// run attack on that file and save real spent in the hash table
		readCount(inFile);
	}
}

int main()
{
    auto start = std::chrono::high_resolution_clock::now();
	int number_identified = 0;
	int number_pass = 1;
	

	while (matched.size() > number_identified || matched.empty()) 
	{
		
        number_identified = matched.size();
	
		// run attack on that file and save real spent in the hash table
		cascade();

		std::cout << "After " << number_pass << "pass, the number of real spent identified is " << 
					matched.size() <<  std::endl;
        std::cout << "And the number of inputs is " << TOTAL_INPUTS << std::endl;
		
		//reset total inputs to zero
		TOTAL_INPUTS = 0;
		number_pass += 1;
	}
	
	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end - start;
	std::cout << elapsed.count() << '\n';
    return 0;
}
