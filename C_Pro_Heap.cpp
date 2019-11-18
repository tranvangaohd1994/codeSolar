#include<iostream>
using namespace std;

#define ll long long

void swap_(ll &a, ll &b) {
	int t = a;
	a = b;
	b = t;
}

//void min_heap(int *a,int lena, int i) {
//	int smallest = i;// chi so cua phan tu nho nhat trong bo 3: node hien tai,node con trai, node con phai
//	int left = i << 1;//vi tri cua node con trai
//	int right = left + 1;//vi tri node con phai
//	if (left <= lena && a[left] < a[i]) smallest = left;
//	if (right <= lena && a[right] < a[smallest]) smallest = right;
//	if (smallest != i) {
//		//swap_(a[i], a[smallest]);//  doi cho 2 phan tu neu neu node cha lon hon node con
//		min_heap(a, lena, smallest);
//	}
//}
//
//void run_minheap(int *a, int lena) {
//	for (int i = lena / 2; i >= 1; i--) {
//		min_heap(a,lena, i);
//	}
//}



const ll maxN = 50000;
ll heap[maxN];
ll test, N, numNode = 0;

//down heap
void downHeap(ll x) {
	ll child = x << 1;
	if (child > numNode) return;
	if (child < numNode && heap[child + 1] < heap[child]) child++; // tim thang nho nhat trong 2 thang con de swap voi cha
	if (heap[x] > heap[child]) {// node parent dang lon hon node con
		swap_(heap[x], heap[child]); // doi cho node con va node cha cho nhau
		downHeap(child); // tiep tuc down heap xuong
	}
}
//delete node root
void del(ll x) {
	heap[x] = heap[numNode];//chuyen node cuoi cung den node can thay the
	numNode--;//giam so node di 1
	downHeap(x);// lam downheap tu vi tri x
}
//update heap
void upHeap(ll index) {
	if (index <= 1)  return;
	ll parent = index / 2; //get node parent
	if (heap[index] < heap[parent]) {
		swap_(heap[index], heap[parent]);
		upHeap(parent);
	}
}

//push 1 element into heap
void push(ll x) {
	numNode++;
	heap[numNode] = x;
	upHeap(numNode);
}

int main() {
	freopen("input_Heap1.txt", "r", stdin);
	cin >> test;
	int inx;
	while (test--) {
		cin >> N;
		numNode = 0;
		for (int i = 1; i <= N; i++) {
			cin >> inx;
			push(inx);
		}
		ll sum = 0,v1,v2;
		for(ll i=1;i<N;i++) {
			v1 = heap[1]; del(1);
			v2 = heap[1]; del(1);
			sum = sum + v1 + v2;
			push(v1+v2);

		}
		cout << sum << endl;
	}

	return 0;
}


///--------------------Hashing -  function------------------------------

#define base 31

#define N  1000007
typedef long long ll;
const ll MOD = 1000000003;

ll hashT[N], p[N];
char T[N],sub[N] ;

ll getHashSub(ll lensub) {
	ll hashSub = 0;
	for (ll i = 1; i <= lensub; i++)
		hashSub = (hashSub * base + sub[i] - 'a' + 1) % MOD;
	return hashSub;
}
ll getHashTij(ll i, ll j) {
	ll r = ((hashT[j] - hashT[i - 1] * p[j - i + 1] + MOD*MOD) % MOD);
	return r;
}
ll getlength(char*s) {
	ll c = 0;
	while (s[c+1])c++;
	return c;
}
int main() {
	freopen("input_DTKSUB.txt", "r", stdin);
	cin >> &T[1];
	cin >> &sub[1];
	ll lenT = getlength(T);
	ll lenSub = getlength(sub);

	hashT[0] = 0;
	for (ll i = 1; i <= lenT; i++) 
		hashT[i] = (hashT[i - 1] * base + T[i] - 'a' + 1) % MOD;

	p[0] = 1;
	for (ll i = 1; i <= lenT; i++)
		p[i] = (p[i - 1] * base) % MOD;
	ll hashSub = getHashSub(lenSub);
	lenT = lenT - lenSub + 1;
	bool flag = false;
	for (ll i = 1; i <= lenT; i++) {
		if (getHashTij(i, i + lenSub - 1) == hashSub) {
			flag = true;
			cout << i << " ";
		}
	}
	if (!flag) cout << " ";
	return 0;
}
