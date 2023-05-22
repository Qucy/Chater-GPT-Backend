// write java class to run below quick sort function
public class Test {

    public static void quicksort(int[] array) {
        // Check if the array is empty or has only one element
        if (array.length <= 1) {
            return array;
        }
        // Select the pivot, which is the element in the middle of the array
        int pivot = array[array.length / 2];
        System.out.println("Pivot: " + pivot);
        // Create a list of elements smaller than the pivot
        int[] left = {x for x in array if x < pivot};
        System.out.println("Left: " + left);
        // Create a list of elements greater than the pivot
        int[] right = {x for x in array if x > pivot};
        System.out.println("Right: " + right);
        // Return the sorted list
        return quicksort(left) + [pivot] + quicksort(right);
    }


    public static void main(String[] args) {
        int[] array = {1, 2, 3, 4, 5, 6, 7, 8, 9};
        int[] sortedArray = Test.quicksort(array);
        System.out.println(sortedArray);
    }
}


