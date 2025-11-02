def get_frequencies():
    print("What are the frequencies of the disease and class?")
    disease_freq = input("Enter the frequency of the disease: ")
    class_freq = input("Enter the frequency of the class: ")

    print("\nSummary:")
    print(f"Frequency of Disease: {disease_freq}")
    print(f"Frequency of Class: {class_freq}")

if __name__ == "__main__":
    get_frequencies()
