#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string> 
#include <unordered_map>


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
	CSVKey input;
	std::string tx = "0";
	int count = 0;

	// go down one row to remove header
	file >> input;

	// open file_out for export
	std::ofstream file_out;
	file_out.open(filename);

	while (file >> input)
	{
		if (count == 0)
		{
			tx = input[4];
		}
		if (input[4] == tx)
		{
			count += 1;
		}
		else
		{
			file_out << tx << "," << count << std::endl;
			tx = input[4];
			count = 1;
		}
	}
	file_out.close();
}

void count_line(std::istream& file, std::string filename) {
	// each row is a input represented by a key in position 2 
	CSVKey input;
	std::string tx = "0";
	int count = 0;
	std::string line;
	std::vector<std::string> v;

	// go down one row to remove header
	
	while (std::getline(file, line, ','))
	{
		count += 1;
	}

	std::cout << count << std::endl;
}


void zero_mixin(std::istream& file, std::istream& transactions) {

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
	std::ifstream  file("C:\\Users\\Xavier\\monero\\data\\test_monero_data_mp300_500.csv");
	std::ifstream transaction("C:\\Users\\Xavier\\monero\\data\\transactions.csv");
	int real_spent_count = 0;
	int total = 0;
	int new_match = 1;
	int t = 1;
	int count = 0;
	std::ios::sync_with_stdio(false);
	std::string line;
	std::vector<std::string> v;

	//count_line(file, "out");

	while (std::getline(file, line))
	{
		v.push_back(line);
	}

	std::cout << v.size() << '\n';

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