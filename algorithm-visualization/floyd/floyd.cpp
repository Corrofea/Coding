#include<bits/stdc++.h>
using namespace std;
int n, m;
const int maxx = 1e2 + 5;
int dis[maxx][maxx];
void init(){
    memset(dis, 0x3f, sizeof(dis));
    cin >> n >> m;
    for (int i = 1; i <= n;i++)
        dis[i][i] = 0;
    int u, v, w;
    for (int i = 1; i <= m; i++) {
        cin >> u >> v;
        cin >> w;
        dis[u][v] = min(w, dis[u][v]);
        dis[v][u] = dis[u][v];
    }
}
void floyd(){
    for (int k = 1; k <= n;k++)
        for (int i = 1; i <= n;i++)
            for (int j = 1; j <= n;j++)
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j]);
}
void print(){
    for (int i = 1; i <= n;i++){
        for (int j = 1; j <= n;j++){
            cout << dis[i][j] << " ";
        }
        cout << endl;
    }
}
int main() {
    init();
    floyd();
    print();
    return 0;
}