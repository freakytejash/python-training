s1 = int(input("Subject 1 marks: "))
s2 = int(input("Subject 2 marks: "))
s3 = int(input("Subject 3 marks: "))
total = s1 + s2 + s3
print("Total marks:", total)
percentage = (total / 300) * 100
print("Percentage:", percentage, "%")
if percentage >= 90:
    print("Grade: A")
elif percentage >= 80:
    print("Grade: B")
elif percentage >= 70:
    print("Grade: C")
elif percentage >= 60:
    print("Grade: D")
else:
    print("Grade: F")
