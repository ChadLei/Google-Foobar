'''
Oh no! Commander Lambda's latest experiment to improve the efficiency of her LAMBCHOP doomsday device has backfired spectacularly. She had been improving the structure of the ion flux converter tree, but something went terribly wrong and the flux chains exploded. Some of the ion flux converters survived the explosion intact, but others had their position labels blasted off. She's having her henchmen rebuild the ion flux converter tree by hand, but you think you can do it much more quickly - quickly enough, perhaps, to earn a promotion!

Flux chains require perfect binary trees, so Lambda's design arranged the ion flux converters to form one. To label them, she performed a post-order traversal of the tree of converters and labeled each converter with the order of that converter in the traversal, starting at 1. For example, a tree of 7 converters would look like the following:

      7
    /   \
  3      6
 /  \   / \
1   2  4   5

Write a function answer(h, q) - where h is the height of the perfect tree of
converters and q is a list of positive integers representing different flux
converters - which returns a list of integers p where each element in p is the
label of the converter that sits on top of the respective converter in q, or -1
if there is no such converter.

For example, answer(3, [1, 4, 7]) would return
the converters above the converters at indexes 1, 4, and 7 in a perfect binary
tree of height 3, which is [3, 6, -1].
'''


from collections import OrderedDict

def solution(h, q):
	def dfs(subtreeSize, offset):
		# We've hit the bottom when there are no more nodes in our subtree, meaning we have visited every node.
		if subtreeSize < 1: return
		# Shifting the size by 1 is the same as dividing it in half, and we do this each time we want to visit the next level since every level has (n - 1)/2 nodes.
		subtreeSize = subtreeSize >> 1
		# Offset is 0 if we're visiting the left subtree. Offset is the number of nodes on the left subtree of the root if we're visiting the left subtrees of the right subtree of the root.
		leftNode = offset + subtreeSize
		# Values on the right subtree are the same as the values on the left + the number of nodes in its subtree (including itself) since we traverse nodes in exactly the same order for both subtrees.
		rightNode = leftNode + subtreeSize
		# The parent node is visited last in a post order traversal so it's just the top node on the right subtree + 1.
		parentNode = rightNode + 1
		# We set the parent node if we're currently visiting the converter we were looking for in q and only change it on the first visit.
		if leftNode in parentLabels and parentLabels[leftNode] == -1:
			parentLabels[leftNode] = parentNode
		if rightNode in parentLabels and parentLabels[rightNode] == -1:
			parentLabels[rightNode] = parentNode
		# We recursively visit the left and right subtrees in order to make sure we cover all converters.
		dfs(subtreeSize, offset)
		dfs(subtreeSize, leftNode)

	# The max amount of nodes in a perfect binary tree has 2^h - 1 nodes.
	maxSize = (2**h) - 1
	# Initialize all converters to -1, which should change later if a valid parent is found.
	parentLabels = OrderedDict((converter,-1) for converter in q)
	# As we go down each level in the tree, each subtree at the level has (n - 1)/2 nodes.
	subtreeSize = maxSize
	# Since we're traversing the whole tree once and setting values as we go, we get a O(n) runtime where n is the amount of total nodes,
	# as compared to looping through each converter in q and running through the whole tree every time to find it which would be O(len(q) * n).
	dfs(subtreeSize, 0)
	return list(parentLabels.values())



t1 = [3, [7, 3, 5, 1]]
t2 = [5, [19, 14, 28]]

print(solution(t2[0], t2[1]))

# Great explaination: https://gist.github.com/dishbreak/48bca2c9c60420a53920c39e08d16c56
