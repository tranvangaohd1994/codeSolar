//------------------Trie - NKSEV spoj---------------------------
#include<iostream>
using namespace std;

const int ALPHA = 26;
const int maxL = 300009, MOD = 1337377;
int N;

//define type Trie node
typedef struct TrieNode {
	bool isEnd;
	TrieNode *childrend[ALPHA];
}TrieNode;

//init node trie
TrieNode* initNode() {
	TrieNode *p = new TrieNode();
	p->isEnd = false;
	for (int i = 0; i < ALPHA; i++)
		p->childrend[i] = NULL;
	return p;
}
// insert word into trie
void insert(TrieNode* root, char *word) {
	TrieNode *proot = root;
	int lenw = 0,id;
	while (word[lenw]){
		id = word[lenw] - 'a';
		if (proot->childrend[id] == NULL) {
			proot->childrend[id] = initNode();
		}
		proot = proot->childrend[id];
		lenw++;
	}
	proot->isEnd = true;//mark last node as leaf

}
bool search(TrieNode *root, char*word) {
	int lenw = 0, id;
	TrieNode *pr = root;
	while (word[lenw]) {
		id = word[lenw] - 'a';
		if (pr->childrend[id] == NULL)
			return false;
		pr = pr->childrend[id];
		lenw++;
	}
	return pr->isEnd;
}
char s[maxL], w[109];
int f[maxL];

int main() {
	freopen("input_NKSEV.txt", "r", stdin);
	TrieNode* root = initNode();
	cin >> s >> N;
	for (int i = 0; i < N; i++) {
		cin >> w;
		insert(root, w);
	}
	int lens = 0, id;
	TrieNode* p = root;
	while (s[lens++]) {}; lens--;
	f[lens] = 1;
	for (int i = lens - 1; i >= 0; i--) {
		p = root;//moi lan lap p tro lai ve root
		for(int j=i;j<lens;j++){
			id = s[j] - 'a';
			if (p->childrend[id] == NULL) break;
			p = p->childrend[id];
			if (p->isEnd) f[i] += f[j + 1];
		}
		f[i] = f[i] % MOD;
	}
	cout << f[0] << endl;

	
	return 0;
}
