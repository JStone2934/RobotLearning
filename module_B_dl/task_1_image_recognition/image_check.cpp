#include <fstream>
#include <iostream>
#include <string>
#include <vector>

const std::string DEFAULT_IMAGE = "/home/unitree/training_camp/module_B_dl/";
const std::vector<std::string> BLESSING_LINES = {
    "恭喜你成功识别到这张祝福图片。",
    "愿新的训练任务顺利完成，代码一路通过。"
};

bool startsWith(const std::vector<unsigned char>& data,
                const std::vector<unsigned char>& pattern) {
    if (data.size() < pattern.size()) {
        return false;
    }

    for (std::size_t i = 0; i < pattern.size(); ++i) {
        if (data[i] != pattern[i]) {
            return false;
        }
    }

    return true;
}

std::string detectImageType(const std::vector<unsigned char>& header) {
    if (startsWith(header, {0x89, 'P', 'N', 'G', 0x0D, 0x0A, 0x1A, 0x0A})) {
        return "PNG image";
    }
    if (startsWith(header, {0xFF, 0xD8, 0xFF})) {
        return "JPEG image";
    }
    if (startsWith(header, {'G', 'I', 'F', '8', '7', 'a'}) ||
        startsWith(header, {'G', 'I', 'F', '8', '9', 'a'})) {
        return "GIF image";
    }
    if (startsWith(header, {'B', 'M'})) {
        return "BMP image";
    }
    if (header.size() >= 12 &&
        header[0] == 'R' && header[1] == 'I' && header[2] == 'F' && header[3] == 'F' &&
        header[8] == 'W' && header[9] == 'E' && header[10] == 'B' && header[11] == 'P') {
        return "WEBP image";
    }

    return "Unknown image format";
}

int main(int argc, char* argv[]) {
    std::string imagePath = argc > 1 ? argv[1] : DEFAULT_IMAGE;

    std::ifstream imageFile(imagePath, ____);
    if (!imageFile) {
        std::cerr << "Error: image file not found: " << imagePath << std::endl;
        return 1;
    }

    std::vector<unsigned char> header(16);
    imageFile.read(reinterpret_cast<char*>(header.data()), header.size());
    header.resize(static_cast<std::size_t>(imageFile.gcount()));

    imageFile.clear();
    imageFile.seekg(0, std::ios::end);
    std::streamoff fileSize = imageFile.tellg();

    std::string imageType = ____(header);

    std::cout << "===== Image Check Result =====" << std::endl;
    std::cout << "Image path : " << imagePath << std::endl;
    std::cout << "File size  : " << fileSize << " bytes" << std::endl;
    std::cout << "Image type : " << imageType << std::endl;
    std::cout << "Message    :" << std::endl;
    for (const std::string& line : BLESSING_LINES) {
        std::cout << "  " << line << std::endl;
    }

    return 0;
}
