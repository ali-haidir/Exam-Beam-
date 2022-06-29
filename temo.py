# Python3 implementation of the approach

# Function that return true if the
# required array can be generated
# with m as the last element
def check(m, n, arr):
    # Build the desired array
    desired = [0] * n;
    for i in range(n - 1, -1, -1):
        desired[i] = m;
        m -= 1;

    # Check if the given array can
    # be converted to the desired array
    # with the given operation
    for i in range(n):
        if (arr[i] > desired[i] or desired[i] < 1):
            return False;

    return True


# Function to return the minimum number
# of operations required to convert the
# given array to an increasing AP series
# with common difference as 1
def minOperations(arr):
    n = len(arr)

    start = arr[n - 1]
    end = max(arr) + n
    max_arr = 0;

    # Apply Binary Search
    while (start <= end):
        mid = (start + end) // 2;

        # If array can be generated with
        # mid as the last element
        if (check(mid, n, arr)):

            # Current ans is mid
            max_arr = mid;

            # Check whether the same can be
            # achieved with even less operations
            end = mid - 1;

        else:
            start = mid + 1;

    # Build the desired array
    desired = [0] * n;
    for i in range(n - 1, -1, -1):
        desired[i] = max_arr;
        max_arr -= 1;

    # Calculate the number of
    # operations required
    operations = 0;
    for i in range(n):
        operations += (desired[i] - arr[i]);

    # Return the number of
    # operations required
    return operations;


# Driver code
if __name__ == "__main__":
    arr = [4, 4, 5, 5, 7];
    # 	n = len(arr);

    print(minOperations(arr));

# This code is contributed by AnkitRai01
