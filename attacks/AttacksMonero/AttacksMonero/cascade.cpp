#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string> 
#include <unordered_map>
#include <chrono>
  

struct Input {
	std::string tx;
	std::string key;
};


class CSVKey
{
public:
	std::string const& operator[](std::size_t index) const
	{
		return m_data[index];
	}
	std::size_t size() const
	{
		return m_data.size();
	}
	void readNextRow(std::istream& str)
	{
		std::string         line;
		std::getline(str, line);

		std::stringstream   lineStream(line);
		std::string         cell;

		m_data.clear();

		while (std::getline(lineStream, cell, ','))
		{
			m_data.push_back(cell);
		}
		// This checks for a trailing comma with no data after it.
		if (!lineStream && cell.empty())
		{
			// If there was a trailing comma then add an empty element.
			m_data.push_back("");
		}
	}
private:
	std::vector<std::string>    m_data;
};


std::istream& operator>>(std::istream& str, CSVKey& data)
{
	data.readNextRow(str);
	return str;
}

// hash table to register real-spent key
std::unordered_map<std::string, int> matched;

void number_transaction(std::istream& file, std::string filename) {
	// each row is a input represented by a key in position 2 
	std::string input;
	std::vector<std::string> transaction;
	std::string tx = "0";
	int count = 0;

	// go down one row to remove header
	std::getline(file, input);

	// read the file 
	while (std::getline(file, input))
	{
		transaction.push_back(input);
	}

	// open file_out for export
	std::ofstream file_out;
	file_out.open(filename);

	// count transactions
	

	while (file >> input)
	{
		if (count == 0)
		{
			tx = input[4];
		}
		//if (input[4] == tx)
		//{
		//	count += 1;
		//}
		else
		{
			file_out << tx << "," << count << std::endl;
			tx = input[4];
			count = 1;
		}
	}
	file_out.close();
}

void count_line(std::ifstream& file, std::string filename) {
	// each row is a input represented by a key in position 2 
	std::string line;
	std::vector<std::string> v;
    std::vector<Input> data;
	//std::ios::sync_with_stdio(false);
	Input input;

	// go down one row to remove header
	std::getline(file, line);
	std::string temp;
	
	while (std::getline(file, line) && !line.empty())
	{
		std::stringstream lineStream(line);

		// this is not great: skipping the first two fields which are not useful
		std::getline(lineStream, temp, ',');
		std::getline(lineStream, temp, ',');

		// get key and transactions
		std::getline(lineStream, input.key, ',');
		std::getline(lineStream, input.tx, ',');
		data.push_back(input);
	}

	std::cout << data[0].tx << '\n';

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
	int test = 0;
	std::string key_identified;
	
	int number_identified = -1;

	while (matched.size() > 1)
	{
		std::cout << "iteration " << '\n';
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

		std::cout << matched.size() << '\n';
	}
	
}


void zero_mixin(std::ifstream& file, std::ifstream& transactions) {

	// each row is a input represented by a key in position 2 
	CSVKey input;
	CSVKey tran;
	std::string key;
	std::string key_identified;
	int count = 0;
	int number_tx = 0;
	int counter_inputs = 1;
	
	// go down one row to remove header
	file >> input;

	while (transactions >> tran) {
		number_tx = std::stoi(tran[1]);
		
		while (counter_inputs <= number_tx)
		{
			file >> input;
			counter_inputs += 1;
			
			// temporarily save all keys in this transaction
			// and count the ones already matched
			key = input[3];
			while ((matched.find(key) == matched.end()) & (count < 1))
			{
				count += 1;
				key_identified = key;
			}
		}
		
		// within a transaction look for key already match
			
		if (count == 1) 
		{
			matched[key_identified] = 1;
		}
		
		// reset counter_transaction and real-spent count
		counter_inputs = 1;
		count = 0;
		
	}
}
int main()
{
	std::ifstream  file("C:\\Users\\MX\\Documents\\Xavier\\Monero\\data\\test_monero_data_mp1100_1200.csv");
	std::ifstream transaction("C:\\Users\\MX\\Documents\\Xavier\\Monero\\data\\transactions.csv");
	int real_spent_count = 0;
	int total = 0;
	int new_match = 1;
	int t = 1;
	int count = 0;
	
	std::string line;
	std::vector<std::string> v;

	auto start = std::chrono::high_resolution_clock::now();
	count_line(file, "transaction");
	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end - start;
	std::cout << elapsed.count() << '\n';

	//while (std::getline(file, line))
	//{
	//	std::cout << "hello" << '\n';
	//	v.push_back(line);
	//	count += 1;
	//	line.clear();
	//}

	

	//while (matched.size() > real_spent_count)
	//{
		//zero_mixin(file, transaction);
		//new_match = matched.size();
		//std::cout << "At iteration " << t << std::endl;
		//std::cout  << "the total inputs is : " << total << std::endl;
		//std::cout << "the total de-anonimized is : " << new_match << std::endl;
		
		//real_spent_count = new_match;
		//t += 1;
	//}
	return 0;
}