
def KiemTraDoiNgau(a, b): #Kiểm tra 2 literal a và b có đối ngẫu nhau hay không
    if a[0] == b[0]: #a và b là 2 literal cùng âm
        return False
    if a[0] != '-' and b[0] != '-': #a và b là 2 literal cùng dương
        return False

    #literal a âm và b dương    
    if a[0] == '-':
        a = a[1:];
    else : #literal a dương và b âm
        b = b[1:]
    
    if a == b:
        return True
    return False

#Sắp xếp 1 literal theo thứ tự chữ cái
def Sort(a):
    for i in range(len(a) - 1):
        for j in range(i+1, len(a)):
            ti = a[i]
            tj = a[j]
            if ti[0] == '-':
                ti = ti[1:]
            if tj[0] == '-':
                tj = tj[1:]
            if ti > tj:
                a[i], a[j] = a[j], a[i]

def PL_Resolve(Ci, Cj):
    Ci = Ci.split(" OR ")
    Cj = Cj.split(" OR ")
   
    newClause = [];
    for i in Ci:
        newClause.append(i)
    for j in Cj:
        if not(j in Ci):
            newClause.append(j) 
    count = 0
    for ci in Ci:
        for cj in Cj:
            if KiemTraDoiNgau(ci, cj):   
                count +=1 
                if count == 2: #Kiểm tra xem hợp giải của Ci và Cj cho ra kết quả vô ích
                    return "0"
                newClause.remove(ci)
                newClause.remove(cj)
                break
    if count == 0: #Ci và Cj không đối ngẫu nhau
        return "0"

    if len(newClause) == 0: #Các literal đơn của Ci và Cj đối ngẫu nhau từng đôi một
        return ""

    Sort(newClause)
    result = newClause[0]
    for i in range(1, len(newClause)):
        result = result + ' OR ' + newClause[i]
    return result

def PL_Resolution(file, a, KB):
    a = a.split(" OR ")
    Am = '-'
    for i in range(len(a)):
        if a[i][0] == Am: #Nếu literal đơn âm thì ta đổi dấu của nó
            a[i] = a[i].replace('-', '')
        else: #Nếu literal đơn dương thì thêm vào để thành âm
            a[i] = Am + a[i]

    #Thêm phủ định của kết luận vào trong KB
    for v in a:
        KB.append(v)

    stop = False
    while True:
        temp = []
        for i in range(0, len(KB)):
            for j in range(i+1, len(KB)):
                resolvents = PL_Resolve(KB[i], KB[j])
                if resolvents == "0": #KB[i] và KB[j] không đối ngẫu nhau hoặc tạo ra literal không có ý nghĩa
                    continue
                if resolvents == "":
                    if stop == False:
                        temp.append("{}")
                    stop = True
                else:
                    temp.append(resolvents)

        test = []
        for v in temp:
            if not(v in KB) and not (v in test):
                test.append(v)

        if len(test) == 0:
            file.write("0\n")
            return False

        file.write(str(len(test)) + '\n')
        for u in test:
            KB.append(u)
            file.write(u + '\n')

        if stop == True:
            return True


def main(fileInput, fileOutput):     
    fileIn = open(".\\Input\\" + fileInput, "r")
    content = []

    for x in fileIn:
        content.append(x)

    for i in range(len(content) - 1):
        content[i] = content[i][:-1]

    a = content[0]
    n = int(content[1])
    KB = []
    for i in range(n):
        KB.append(content[2 + i])

    fileOut = open(".\\Output\\" + fileOutput, "w")
    if PL_Resolution(fileOut, a, KB):
        fileOut.write("YES")
    else:
        fileOut.write("NO")   
        
if __name__ == "__main__":
    fileInputs = ["Input1.txt", "Input2.txt","Input3.txt","Input4.txt","Input5.txt"]
    fileOutputs = ["Output1.txt", "Output2.txt", "Output3.txt", "Output4.txt", "Output5.txt"]

    for i in range(len(fileInputs)):
        main(fileInputs[i], fileOutputs[i])
