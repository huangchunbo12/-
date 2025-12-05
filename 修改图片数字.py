import os
import re


def rename_mixed_images(folder_path):
    if not os.path.exists(folder_path):
        print(f"错误：找不到路径 {folder_path}")
        return

    # 正则表达式：匹配纯数字文件名 (例如 1.jpg, 23.jpg)
    # ^ 表示开头, \d+ 表示一个或多个数字, \.jpg$ 表示以 .jpg 结尾
    # re.IGNORECASE 让它对 .JPG 也生效
    number_pattern = re.compile(r'^\d+\.jpg$', re.IGNORECASE)

    files = os.listdir(folder_path)

    # 1. 先统计哪些数字已经被占用了，以及哪些文件需要改名
    used_numbers = set()
    files_to_rename = []

    print(f"正在扫描文件夹: {folder_path}")
    print("-" * 30)

    for filename in files:
        # 忽略文件夹，只看文件
        if not os.path.isfile(os.path.join(folder_path, filename)):
            continue

        # 特殊文件：top.jpg 直接跳过
        if filename.lower() == 'top.jpg':
            print(f"[保留] 特殊文件: {filename}")
            continue

        # 判断是否为 jpg
        if filename.lower().endswith('.jpg'):
            # 使用正则判断：如果是纯数字文件名
            if number_pattern.match(filename):
                # 提取数字部分并记录 (例如 "12.jpg" -> 12)
                num = int(os.path.splitext(filename)[0])
                used_numbers.add(num)
                print(f"[保留] 纯数字文件: {filename}")
            else:
                # 既不是 top.jpg，也不是纯数字，加入待修改列表
                files_to_rename.append(filename)

    # 对待修改的文件排序，保证顺序一致
    files_to_rename.sort()

    print("-" * 30)

    if not files_to_rename:
        print("没有需要修改的文件。")
        return

    # 2. 开始重命名
    # 从 1 开始尝试，寻找未被使用的数字
    current_num = 1

    for old_filename in files_to_rename:
        # 如果 current_num 已经被占用了（在 used_numbers 里），就+1，直到找到一个空缺的数字
        while current_num in used_numbers:
            current_num += 1

        new_name = f"{current_num}.jpg"
        old_path = os.path.join(folder_path, old_filename)
        new_path = os.path.join(folder_path, new_name)

        try:
            os.rename(old_path, new_path)
            print(f"[重命名] {old_filename} -> {new_name}")

            # 标记这个新数字已被占用
            used_numbers.add(current_num)
        except Exception as e:
            print(f"[错误] 重命名 {old_filename} 失败: {e}")

    print("-" * 30)
    print("处理完成！")


if __name__ == "__main__":
    target_path = r"C:\public\photos"
    rename_mixed_images(target_path)