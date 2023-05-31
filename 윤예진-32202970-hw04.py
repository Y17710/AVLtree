"""
알고리즘 1분반 소프트웨어학과 32202970 윤예진 
HW4 - AVL 트리 구현
"""

# 노드 클래스 선언
class TreeNode:
    def __init__(self, val):
        self.val = val              # 노드의 값
        self.left = None
        self.right = None
        self.parent = None
        self.height = -100


# AVL 트리 클래스
# 주요 연산 기능
# 재균형 - reBalance()
# 삽입 - insert()
# 삭제 - delete()
# 탐색 - search()
# 출력 - print()
class AVL_Tree:
    def __init__(self):
        self.root = None
    
    # 균형을 검사하여 재균형 맞추는 함수
    def reBalance(self, parent):
        if(parent is None):
            return
        
        hDiff = self.calc_height_diff(parent)
        
        # 균형 인수의 절댓값이 2이상일 때
        # 왼쪽 서브트리로 기울어진 경우
        if hDiff > 1:
            if self.calc_height_diff(parent.left) > 0:
                parent = self.rotateLL(parent)
            else: parent = self.rotateLR(parent)
        # 오른쪽 서브트리로 기울어진 경우
        elif hDiff < -1:
            if self.calc_height_diff(parent.right) < 0:
                parent = self.rotateRR(parent)
            else: parent = self.rotateRL(parent)
        
        if(parent is not None):
            self.reBalance(parent.parent)
        
        return parent
    
    # LL 로테이션
    def rotateLL(self, A):
        print("LL rotation: node %d (BF: %d)" %(A.val, self.calc_height_diff(A)))
        B = A.left
        A.left = B.right
        B.right = A
        
        # 회전 후 각 노드의 부모에 대한 포인터 갱신, 부모 노드의 자식 노드 포인터 갱신
        if(A.left is not None):
            A.left.parent = A
        B.parent = A.parent
        if(self.root == A):
            self.root = B
        else:
            if(B.parent.left == A):
                B.parent.left = B
            elif(B.parent.right == A):
                B.parent.right = B
        A.parent = B
        
        # 노드별 높이 조정
        A.height = self.calc_height(A)
        B.height = self.calc_height(B)

        return B
    
    # RR 로테이션
    def rotateRR(self, A):
        print("RR rotation: node %d (BF: %d)" %(A.val, self.calc_height_diff(A)))
        B = A.right
        A.right = B.left
        B.left = A
        
        # 회전 후 각 노드의 부모에 대한 포인터 갱신, 부모 노드의 자식 노드 포인터 갱신
        if(A.right is not None):
            A.right.parent = A
        B.parent = A.parent
        if(self.root == A):
            self.root = B
        else:
            if(B.parent.left == A):
                B.parent.left = B
            elif(B.parent.right == A):
                B.parent.right = B
        A.parent = B
        
        # 노드별 높이 조정
        A.height = self.calc_height(A)
        B.height = self.calc_height(B)
        
        return B
    
    # RL 로테이션
    def rotateRL(self, A):
        print("RL rotation: node %d (BF: %d)" %(A.val, self.calc_height_diff(A)))
        B = A.right
        print("(RL rotation)", end='')
        A.right = self.rotateLL(B)
        print("(RL rotation)", end='')
        return self.rotateRR(A)
    
    # LR 로테이션
    def rotateLR(self, A):
        print("LR rotation: node %d (BF: %d)" %(A.val, self.calc_height_diff(A)))
        B = A.left
        print("(LR rotation)", end='')
        A.left = self.rotateRR(B)
        print("(LR rotation)", end='')
        return self.rotateLL(A)
    
    
    # AVL트리에 새로운 노드를 삽입하는 함수
    def insert(self, val):
        # 트리에 노드가 존재하지 않을 경우 루트노드로 설정
        if (self.root is None):
            self.root = TreeNode(val)
            self.root.height = 0
            return
        
        parent = self.root
        # 빈 자리를 찾을 때까지 노드(parent)와 비교
        while(parent is not None):
            # 중복된 값
            if(parent.val == val):
                print("키 값 중복")
                return
            # 노드보다 클 경우
            elif(parent.val < val):
                # 빈자리가 있을 경우
                if(parent.right is None):
                    newNode = TreeNode(val)
                    newNode.parent = parent
                    newNode.height = 0
                    parent.right = newNode
                    self.reBalance(parent)
                    self.root.height = self.calc_height()
                    if(self.root.val < val):
                        self.setHeight(self.root.right)
                    elif(self.root.val > val):
                        self.setHeight(self.root.left)
                    return
                # 빈자리가 없을 경우 다시 비교
                else:
                    parent = parent.right
                    continue
            # 노드보다 작을 경우
            elif(parent.val > val):
                # 빈자리가 있을 경우
                if(parent.left is None):
                    newNode = TreeNode(val)
                    newNode.parent = parent
                    newNode.height = 0
                    parent.left = newNode
                    self.reBalance(parent)
                    self.root.height = self.calc_height()
                    if(self.root.val < val):
                        self.setHeight(self.root.right)
                    elif(self.root.val > val):
                        self.setHeight(self.root.left)
                    return
                # 빈자리가 없을 경우 다시 비교
                else:
                    parent = parent.left
                    continue
       
    
    # 노드를 삭제하는 함수    
    def delete(self, root, key):
    # 루트 노드가 공백이라면 None 반환
        if root == None:
            return None
    
        parent = None                   # 삭제할 노드의 부모 노드
        node = root                     # 삭제할 노드
    
        # 삭제할 노드(node)/부모노드(parent) 탐색
        while (node != None and node.val != key):
            parent = node
            # 키값 < 노드 키값 이라면, 왼쪽 서브트리 탐색
            if (key < node.val): node = node.left
            # 키값 > 노드 키값 이라면, 오른쪽 서브트리 탐색
            else: node = node.right
    
        # 삭제할 노드가 없을 경우
        if node == None: return None
        # 리프 노드일 경우
        if (node.left == None and node.right == None):
            root = self.delete_case1(parent, node, root)
        # 자식 노드를 하나만 가질 경우
        elif (node.left == None or node.right == None):
            root = self.delete_case2(parent, node, root)
        # 자식 노드가 두개일 경우    
        else:
            root = self.delete_case3(parent, node, root)
            
        # BF 재설정
        self.reBalance(parent)
        return root


    # 리프노드를 삭제하는 함수
    def delete_case1(self, parent, node, root):
    # 해당 노드가 루트라면, 공백 트리
        if parent is None:
            root = None
        else:
            # 삭제할 노드가 부모노드의 왼쪽 자식이라면
            if parent.left == node:
                parent.left = None
            # 삭제할 노드가 부모노드의 왼쪽 자식이라면
            elif parent.right == node:
                parent.right = None
            
        return root


    # 삭제할 노드가 한개의 자식 노드를 가질 경우, 노드를 삭제하는 함수
    def delete_case2(self, parent, node, root):
        # 자식 노드
        if node.left is not None:
            child = node.left
        else:
            child = node.right
    
        # 루트 노드를 삭제할 경우, 자식 노드를 루트 노드로 한다
        if node == root:
            root = child
        else:
            # 삭제할 노드가 부모 노드의 왼쪽 자식이라면, 해당 자리에 삭제할 노드의 자식 노드를 연결
            if node is parent.left:
                parent.left = child         
            # 삭제할 노드가 부모 노드의 오른쪽 자식이라면, 해당 자리에 삭제할 노드의 자식 노드를 연결
            else: parent.right = child
            
        return root


    # 삭제할 노드가 두개의 자식 노드를 가질 경우, 노드를 삭제하는 함수
    # 오른쪽 서브트리의 최솟값을 후계자로 한다
    def delete_case3(self, parent, node, root):
        succp = node                    # 후계자 노드
        succ = node.right               # 후계자 노드의 부모노드
    
        # 후계자와 부모노드 탐색
        while(succ.left != None):
            succp = succ
            succ = succ.left
    
        # 후계자가 왼쪽 자식이면, 후계자의 오른쪽 자식을 후계자 부모의 왼쪽에 연결
        if(succp.left == succ):
            succp.left = succ.right
        # 후계자가 오른쪽 자식이면(삭제할 노드가 루트 노드일 경우), 후계자의 오른쪽 자식을 후계자 부모의 오른쪽에 연결
        else:
            succp.right = succ.right
        
        node.key = succ.key             # 후계자의 키, 값을 삭제할 노드에 복사
        node.data = succ.data
    
        return root
    
    
        # 루트 노드(root)로부터의 높이를 계산하는 함수
    def calc_height(self, root=None):
        if(root is None):
            root = self.root
        
        hLeft = 0
        hRight = 0
        
        if(root.left is not None):
            hLeft = self.calc_height(root.left)
        if(root.right is not None):
            hRight = self.calc_height(root.right)
        if(root.left is None and root.right is None):
            return 0
        
        if(hLeft > hRight):
            return hLeft + 1
        elif(hLeft < hRight):
            return hRight + 1
        else:
            return hLeft + 1
        
    
    # 루트(root)의 왼쪽 서브트리와 오른쪽 서브트리 높이 차이를 계산하여 반환하는 함수
    def calc_height_diff(self, root=None):
        if(root is None):
            root = self.root
        hLeft = 0
        hRight = 0

        if(root.left is not None):
            hLeft = self.calc_height(root.left) + 1
        if(root.right is not None):
            hRight = self.calc_height(root.right) + 1
        
        return hLeft-hRight
    
       
    # 트리에 변경사항이 있을때마다 높이를 갱신하는 함수
    # root와 root의 서브트리에 대해 갱신을 진행한다
    def setHeight(self, root):
        if(root is None):
            return
        
        root.height = self.calc_height(root)
        self.setHeight(root.left)
        self.setHeight(root.right)
        
        
    # 어떤 노드와 그 서브 트리에 대해 탐색 연산
    # 전체 트리 검사 시 루트 노드를 인자로 전달 필요
    def search(self, key, node):
        if(node.val == key):
            return node
        elif(node.val > key):
            node = node.left
        elif(node.val < key):
            node = node.right
            
        if(node == None):
            return False
        else:
            self.search(key, node)
    

    # 루트 노드(레벨0)부터 시작하여 레벨 별로 AVL 트리를 출력하는 함수
    def print(self):
        queue = list()                  # 리스트를 활용하는 큐
        queue.append(self.root)
        level = 0
        count = 0
        print("\nLevel 0 :", end='\t')
        # 큐가 공백이 아닌 동안
        while len(queue):
            # 해당 레벨의 모든 노드를(None 포함) 출력하면 레벨 갱신
            if(count == pow(2, level)):
                count = 0
                level += 1
                print("\nLevel %d :" %(level), end='\t')
                
            n = queue.pop(0)
            if n is not None:
                print("[v:%d]" %(n.val), end='\t')
                queue.append(n.left)
                queue.append(n.right)
            elif n is None:
                print("[None]", end='\t')
            count += 1
        print('\n')
    