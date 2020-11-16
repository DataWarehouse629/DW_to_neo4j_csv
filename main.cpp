#include <iostream>
#include <fstream>
#include <chrono>
#include <string>
#include <algorithm>

#define SHOW_CONTENT true
#undef SHOW_CONTENT

inline bool is_space_line(const std::string& str){
    return str.length() == 0;
}

inline bool is_id_line(const std::string& str){
    return str[0] == 'p';
}

size_t get_file_size(const std::string& file_path) {
    std::ifstream file(file_path);
    file.seekg(0, std::ios::end);
    const auto file_size = file.tellg();
    file.close();
    return file_size;
}


int main() {
    const std::string raw_file_path = R"(./movies.txt)";
    const std::string user_file_path = "./user.csv";
    const std::string reviews_file_path = "./reviews.csv";


    std::ifstream raw_file(raw_file_path, std::ios::binary);
    std::ofstream user_file(user_file_path);
    std::ofstream reviews_file(reviews_file_path);

    user_file << "userId:ID,profileName:string[]" << std::endl;
    reviews_file << ":START_ID(userId),:END_ID(productId)" << std::endl;
    
    std::ofstream log ("log.txt");

    const std::string k_label_product("product/productId: ");
    const std::string k_label_user("review/userId: ");
    const std::string k_label_name("review/profileName: ");
    const auto k_product_start = k_label_product.length();
    const auto k_user_start = k_label_user.length();
    const auto k_name_start = k_label_name.length();

    const size_t file_size = get_file_size(raw_file_path);
    size_t char_count = 0;
    size_t line_count = 0;
    size_t comment_count = 0;
    size_t product_count = 0;
    size_t file_count = 0;
    size_t review_count = 0;

    std::string line;

    while (raw_file) {
        std::getline(raw_file, line);
#ifdef SHOW_CONTENT
        std::cout << line << std::endl;
#endif
        if (is_id_line(line)) {
            std::string product_id = line.substr(k_product_start);
            std::getline(raw_file, line);
            std::string user_id = line.substr(k_user_start);
           
            std::getline(raw_file, line);
            std::string profile_name = line.substr(k_name_start);
            std::replace(profile_name.begin(), profile_name.end(), '\n', ' '); 
            user_file << user_id << ","  << profile_name << "\n"; 
            reviews_file << user_id << "," <<  product_id << "\n";     
            review_count++;
            do {
                ++line_count;
                std::getline(raw_file, line);
            } while (!is_space_line(line));
        }
        line_count++;
    }
    user_file << std::flush;
    reviews_file << std::flush;
    user_file.close();
    reviews_file.close();
    std::cout << line_count << std::endl;
    std::cout << review_count << std::endl;
    //std::cout << block << std::endl;
    //std::cout << raw_file.tellg() << std::endl;
    return 0;
}
