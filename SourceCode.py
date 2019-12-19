from PyPDF2 import PdfFileWriter, PdfFileReader

def bookmark_dict(bookmark_list):
    """ Used to get the bookmarks form the pdf"""
    result = {}
    for item in bookmark_list:
        if isinstance(item, list):
            # recursive call
            result.update(bookmark_dict(item))
        else:
            result[reader.getDestinationPageNumber(item)] = item.title
    return result



print("Enter path to File(Example:: C:/Bob/Documents/)\n make sure it ends with /:",end='')
pa=input()
print("Enter the PDF file name(Example:: Bob.pdf):",end='')
th=input()
path = pa+th
writer = PdfFileWriter()
reader = PdfFileReader(path)

BookMarks = bookmark_dict(reader.getOutlines())
Total_Number_pages = reader.getNumPages()

Bname = ""
###################### Cleaning Bookmarks
for i in BookMarks.keys():
    Bname = str(BookMarks[i])
    Bname = Bname.replace("b'","")
    Bname = Bname.replace(r"\r'","")
    Bname = Bname.replace("&","AND")
    BookMarks[i] = Bname

######################
j = 0
ListOfList = []
Total_Number_Pages = reader.getNumPages()
for i in range(0,Total_Number_Pages+1):
    if i+1 in BookMarks.keys():
        print("Start Page:{} \tDocument:{} \tEnd Page:{}".format(j+1,BookMarks[j],i+1))
        temp=[]
        temp.append(j)
        temp.append(BookMarks[j])
        temp.append(i)
        ListOfList.append(temp)
        j=i+1
print("Start Page:{} \tDocument:{} \tEnd Page:{}".format(j+1,BookMarks[j],i))
temp=[]
temp.append(j)
temp.append(BookMarks[j])
temp.append(i-1)
ListOfList.append(temp)


oppath = r"{}BookMarks.txt".format(pa)
f=open(oppath,"w")

for i in ListOfList:
    string_to_p = "{}\n".format(i[1])
    f.writelines(string_to_p)
f.close()

print("A new file known as Bookmarks.txt is now created in {}\n got to there to view it".format(pa))

print("\n\nNow you must Make a new text file called NewBookMarks.txt at {}\n".format(pa),
      "Now Rearrange the bookmarks from Bookmarks.txt and paste in NewBookMarks file however you like\n"
      "then press Y ::")
a=input()
if a.upper() == 'Y':
    oppath = r"{}NewBookMarks.txt".format(pa)
    Nf = open(oppath,"r")
    Entire = Nf.read()
    Entire = Entire.replace("++","")
    Entire=Entire.split("\n")
    cnt=len(ListOfList)
    pg=0
    opg=0
    inc=1
    for i in range(len(Entire)):
        print("{}. For {}".format(inc,Entire[i]))
        inc=inc+1
        j = 0
        while j<cnt:
            if Entire[i] == ListOfList[j][1]:
                lb=ListOfList[j][0]
                ub=ListOfList[j][2]
                opg=pg
                print("\t\t{}- {} --> {} at {}".format(lb,ub,ListOfList[j][1],opg))
                for k in range(lb,ub+1):
                    writer.addPage(reader.getPage(k))
                    pg = pg+1
                writer.addBookmark(title=str(ListOfList[j][1]),pagenum=opg,parent=None)
                ListOfList.pop(j)
                cnt = cnt-1
                break
            j=j+1
    print("Write New Pdf File Name(Example: Result.pdf)\n::")
    output_name=input()
    output_name=pa+output_name

    with open(output_name,"wb") as out:
        writer.write(out)


