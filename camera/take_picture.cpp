#include <cstdlib>
#include <iostream>

int main() {
    std::string filename = "test.jpg";

    // Use libcamera-still command to capture an image
    std::string command = "libcamera-still -o " + filename;
    int result = std::system(command.c_str());

    if (result == 0) {
        std::cout << "Image saved as " << filename << std::endl;
    } else {
        std::cerr << "Failed to capture image!" << std::endl;
    }

    return 0;
}
