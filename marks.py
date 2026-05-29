s1 = int(input("Enter marks of subject 1: "))
s2 = int(input("Enter marks of subject 2: "))
s3 = int(input("Enter marks of subject 3: "))

total = s1 + s2 + s3
percentage = (total / 300) * 100

print("Total marks: ", total)
print("Percentage: ", percentage)
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