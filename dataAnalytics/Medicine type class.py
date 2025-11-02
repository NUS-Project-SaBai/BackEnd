def get_common_medicine():
    print("What is the most common type of medicine that is being dispensed and its class?")
    medicine_type = input("Enter the most common type of medicine: ")
    medicine_class = input("Enter the class of this medicine: ")

    print("\nSummary:")
    print(f"Most Common Medicine: {medicine_type}")
    print(f"Medicine Class: {medicine_class}")

if __name__ == "__main__":
    get_common_medicine()
