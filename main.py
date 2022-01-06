import pandas as pd
import re


def concat_df(files):
    list_data_frame = []
    for file in files:
        d = pd.read_csv(file, encoding="utf8", sep="\t")
        try:
            d = d.drop(labels=["Producer"], axis=1)
        except:
            pass
        list_data_frame.append(d)
    df = pd.concat(list_data_frame).drop_duplicates()
    df.to_csv("result1.csv", encoding="utf8", sep="\t", index=False)


def price(text):
    try:
        text = str(text).replace(".", "").replace("₫", "").replace(r'\s+', "")
        return int(text)
    except:
        return "None"


def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s


def process_name(text):
    data = text.split(" ")
    result = ''
    for d in data:
        if d == no_accent_vietnamese(d):
            result += d + ' '
    return result


def process_cpu(CPU):
    remove = ['INTEL CORE ', 'PROCESSOR ', 'AMD ', 'XEON ', 'INTEL CELERON PROCESSOR ', 'APPLE ', 'INTEL CELERON ',
              'INTEL PENTIUM SILVER ', 'INTEL ', 'PENTIUM ', 'PEN ', 'INTELCORE ']
    repl = ['RYZEN ', 'RYZEN', 'AMDR', 'RR']
    result = []
    for cpu in CPU:
        cpu = re.sub(r"[^a-zA-Z0-9\s]", "", cpu.split("(")[0].upper().replace("-", " ")).strip()
        cpu = re.sub("INTEL CORE 5", "INTEL CORE I5", cpu)
        cpu = re.sub("W ", "W", cpu)
        for ele in remove:
            cpu = re.sub(ele, "", cpu)
        for ele in repl:
            cpu = re.sub(ele, "R", cpu)
        cpu = re.sub("COREI", "I", cpu.strip())
        result.append(cpu.split(" ")[0])
    return result


def process_ram(RAM):
    total_ram = []
    for ram in RAM:
        ram = ram.split("GB")[0].strip().replace('*', ' x ')
        if ' x ' in re.sub(r"[^A-Z()]", "", ram):
            temp = ram.split(' x ')
            total_ram.append(int(temp[0]) * int(temp[1]))
        else:
            total_ram.append(int(ram))
    return total_ram


def process_disk(DISK):
    type_disk = []
    capacity_disk = []
    for disk in DISK:
        disk = disk.upper()
        disk = re.sub("M.2 ", "", disk)
        if 'SSD' in disk:
            type_disk.append(1)
        else:
            type_disk.append(0)
        try:
            capacity_disk.append(int(disk.strip().split('GB')[0]))
        except:
            capacity_disk.append(int(disk.strip().split('TB')[0]) * 1024)
    return type_disk, capacity_disk


def process_prices(Old_Price, New_Price):
    res = []
    for i in range(0, len(Old_Price)):
        try:
            old = int(Old_Price[i])
        except:
            old = 0
        try:
            new = int(New_Price[i])
        except:
            new = 0
        res.append(int((old + new) / 2))
    return res


if __name__ == '__main__':
    # noi 3 dataframe
    # files = ['Product_An_Phat.csv', 'Product_HNCom.csv', 'Product_Phong_Vu.csv']
    # concat_df(files)
    # doc dataframe, loai bo gia tri loi
    # data = pd.read_csv('result1.csv', encoding='utf8', sep='\t')
    # for item in ["CPU", 'DISK', 'RAM', 'DISPLAY']:
    #     data = data.loc[data[item] != 'None']
    # data = data.loc[data["CPU"] != 'Microsoft SQ 2']
    # data = data.loc[data["RAM"] != 'LPDDR4x 4266Mhz on board']
    # data = data.dropna()
    # data.to_csv("1.csv", encoding="utf8", sep="\t", index=False)
    data = pd.read_csv('1.csv', encoding='utf8', sep='\t')
    Name = [x.lower() for x in data['Name']]
    CPU = [x for x in data['CPU']]
    RAM = [x for x in data['RAM']]
    DISK = [x for x in data['DISK']]
    GPU = [x for x in data['GPU']]
    DISPLAY = [x for x in data['DISPLAY']]
    Old_Price = [x for x in data['Old Price']]
    New_Price = [x for x in data['New Price']]

    # add product value
    producer = [process_name(x).split(" ")[1] for x in Name]
    # process cpu
    # g = []
    # for gpu in GPU:
    #
    #     g.append(re.sub(r"[^a-zA-Z0-9\s]", "", gpu.strip().upper()))
    # for x in set(g):
    #     print(x)
    a = []
    for display in DISPLAY:
        rep = ['"', '-inch', 'inch']
        for r in rep:
            display = re.sub(r, " inch", display.strip())
        a.append(display.split(" ")[0])
    print(set(a))
