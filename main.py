import os
import sys

from prettytable import prettytable

all_file = []

language_suffix = {}
language_suffix["assembly"] = ["asm"]
language_suffix["c"] = ["c", "h"]
language_suffix["c++"] = ["cpp", "cc", "cxx", "c++", "hpp", "hxx"]
language_suffix["c#"] = ["cs"]
language_suffix["java"] = ["java"]
language_suffix["php"] = ["php"]
language_suffix["perl"] = ["pm", "pl"]
language_suffix["python"] = ["py", "py3"]
language_suffix["kotlin"] = ["kt"]

language_classify = {}
language_classify["assembly"] = []
language_classify["c"] = []
language_classify["c++"] = []
language_classify["c#"] = []
language_classify["java"] = []
language_classify["php"] = []
language_classify["perl"] = []
language_classify["python"] = []
language_classify["kotlin"] = []

file_rows = {}


def GetAllFile(path):
    file_path = []
    all_file_path = os.listdir(path)
    for sub_path in all_file_path:
        new_path = path + "/" + sub_path
        if os.path.isdir(new_path):
            new_sub_path = GetAllFile(new_path)
            file_path = file_path + new_sub_path
        elif os.path.isfile(new_path):
            file_path.append(new_path)
        else:
            print("special file!")
    return file_path


def Classify(files):
    for file in files:
        file_name = os.path.basename(file)
        suffix = file_name.split(".")[-1]
        for std_suffix in language_suffix.keys():
            if suffix in language_suffix[std_suffix]:
                language_classify[std_suffix].append(file)
                break
    return language_classify


def Count(dict):
    for std_suffix in dict:
        files = dict[std_suffix]
        for file in files:
            count = 0
            with open(file, 'rb') as f:
                for line in f:
                    count += 1
            file_rows[file] = count
    return file_rows


def Show(dict_file, dict_rows):
    tb = prettytable.PrettyTable()
    field_names = []
    row = []
    for suffix in dict_file:
        files = dict_file[suffix]
        total_count = 0
        for file in files:
            count = dict_rows[file]
            total_count += count
        if total_count > 0:
            field_names.append(suffix)
            row.append(total_count)
    tb.field_names = field_names
    tb.add_row(row)
    print(tb)


if __name__ == '__main__':
    if (len(sys.argv) != 2):
        print("请合法输入")
    else:
        dir = sys.argv[1]
        print("检测文件夹路径：", dir)
        # 获取所以文件
        all_file = GetAllFile(dir)
        print("目录下文件数量:", len(all_file))
        # 文件分类
        classify = Classify(all_file)
        # 文件行数统计
        rows = Count(classify)
        # 展示图标
        Show(classify, rows)
