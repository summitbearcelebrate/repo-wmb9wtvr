/* ============================================
 * 转转二手交易管理系统
 * 开发语言：C语言
 * 编译环境：GCC / Dev-C++
 * ============================================ */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_USERS 100
#define MAX_PRODUCTS 500
#define MAX_ORDERS 1000
#define NAME_LEN 50
#define DESC_LEN 200
#define DATE_LEN 20

/* ========== 数据结构定义 ========== */
typedef struct {
    int user_id;
    char username[NAME_LEN];
    char password[NAME_LEN];
    char phone[20];
    int role;  // 0-买家 1-卖家 2-管理员
    char reg_date[DATE_LEN];
} User;

typedef struct {
    int product_id;
    char name[NAME_LEN * 2];
    char description[DESC_LEN];
    float price;
    char category[NAME_LEN];
    int seller_id;
    int status;  // 0-下架 1-在售 2-已售
    char pub_date[DATE_LEN];
} Product;

typedef struct {
    int order_id;
    int buyer_id;
    int product_id;
    float price;
    int status;  // 0-待付款 1-已付款 2-已完成 3-已取消
    char order_date[DATE_LEN];
    char complete_date[DATE_LEN];
} Order;

/* ========== 全局变量 ========== */
User users[MAX_USERS];
Product products[MAX_PRODUCTS];
Order orders[MAX_ORDERS];
int user_count = 0;
int product_count = 0;
int order_count = 0;
int current_user_id = -1;  // 当前登录用户ID

/* ========== 工具函数 ========== */
void get_current_date(char *date_str) {
    time_t t = time(NULL);
    struct tm *tm_info = localtime(&t);
    strftime(date_str, DATE_LEN, "%Y-%m-%d", tm_info);
}

void clear_screen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void pause_screen() {
    printf("\n按回车键继续...");
    getchar();
    getchar();
}

/* ========== 文件操作 ========== */
void save_users() {
    FILE *fp = fopen("users.dat", "wb");
    if (fp) {
        fwrite(&user_count, sizeof(int), 1, fp);
        fwrite(users, sizeof(User), user_count, fp);
        fclose(fp);
    }
}

void load_users() {
    FILE *fp = fopen("users.dat", "rb");
    if (fp) {
        fread(&user_count, sizeof(int), 1, fp);
        fread(users, sizeof(User), user_count, fp);
        fclose(fp);
    }
}

void save_products() {
    FILE *fp = fopen("products.dat", "wb");
    if (fp) {
        fwrite(&product_count, sizeof(int), 1, fp);
        fwrite(products, sizeof(Product), product_count, fp);
        fclose(fp);
    }
}

void load_products() {
    FILE *fp = fopen("products.dat", "rb");
    if (fp) {
        fread(&product_count, sizeof(int), 1, fp);
        fread(products, sizeof(Product), product_count, fp);
        fclose(fp);
    }
}

void save_orders() {
    FILE *fp = fopen("orders.dat", "wb");
    if (fp) {
        fwrite(&order_count, sizeof(int), 1, fp);
        fwrite(orders, sizeof(Order), order_count, fp);
        fclose(fp);
    }
}

void load_orders() {
    FILE *fp = fopen("orders.dat", "rb");
    if (fp) {
        fread(&order_count, sizeof(int), 1, fp);
        fread(orders, sizeof(Order), order_count, fp);
        fclose(fp);
    }
}

/* ========== 用户管理模块 ========== */
void user_register() {
    if (user_count >= MAX_USERS) {
        printf("系统用户已满！\n");
        return;
    }
    User new_user;
    new_user.user_id = user_count + 1;
    printf("请输入用户名: ");
    scanf("%s", new_user.username);
    // 检查用户名唯一性
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, new_user.username) == 0) {
            printf("用户名已存在！\n");
            return;
        }
    }
    printf("请输入密码: ");
    scanf("%s", new_user.password);
    printf("请输入手机号: ");
    scanf("%s", new_user.phone);
    printf("请选择角色(0-买家 1-卖家): ");
    scanf("%d", &new_user.role);
    get_current_date(new_user.reg_date);
    users[user_count++] = new_user;
    save_users();
    printf("注册成功！用户ID: %d\n", new_user.user_id);
}

int user_login() {
    char username[NAME_LEN], password[NAME_LEN];
    printf("请输入用户名: ");
    scanf("%s", username);
    printf("请输入密码: ");
    scanf("%s", password);
    for (int i = 0; i < user_count; i++) {
        if (strcmp(users[i].username, username) == 0 &&
            strcmp(users[i].password, password) == 0) {
            current_user_id = users[i].user_id;
            printf("登录成功！欢迎 %s\n", username);
            return 1;
        }
    }
    printf("用户名或密码错误！\n");
    return 0;
}

void user_menu() {
    int choice;
    do {
        clear_screen();
        printf("\n===== 用户管理 =====\n");
        printf("1. 用户注册\n");
        printf("2. 用户登录\n");
        printf("3. 修改信息\n");
        printf("4. 查看信息\n");
        printf("0. 返回主菜单\n");
        printf("请选择: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: user_register(); break;
            case 2: user_login(); break;
            case 3:
                if (current_user_id > 0) {
                    printf("请输入新手机号: ");
                    scanf("%s", users[current_user_id-1].phone);
                    save_users();
                    printf("修改成功！\n");
                } else printf("请先登录！\n");
                break;
            case 4:
                if (current_user_id > 0) {
                    User *u = &users[current_user_id-1];
                    printf("用户ID: %d\n用户名: %s\n手机号: %s\n注册日期: %s\n",
                           u->user_id, u->username, u->phone, u->reg_date);
                } else printf("请先登录！\n");
                break;
        }
        if (choice != 0) pause_screen();
    } while (choice != 0);
}

/* ========== 商品管理模块 ========== */
void publish_product() {
    if (current_user_id <= 0) { printf("请先登录！\n"); return; }
    if (product_count >= MAX_PRODUCTS) { printf("商品数量已满！\n"); return; }
    Product p;
    p.product_id = product_count + 1;
    p.seller_id = current_user_id;
    p.status = 1;
    printf("请输入商品名称: ");
    scanf("%s", p.name);
    printf("请输入商品描述: ");
    scanf("%s", p.description);
    printf("请输入商品价格: ");
    scanf("%f", &p.price);
    printf("请输入商品分类: ");
    scanf("%s", p.category);
    get_current_date(p.pub_date);
    products[product_count++] = p;
    save_products();
    printf("商品发布成功！商品ID: %d\n", p.product_id);
}

void browse_products() {
    printf("\n===== 在售商品列表 =====\n");
    printf("%-5s %-15s %-10s %-10s %-10s\n", "ID", "名称", "价格", "分类", "发布日期");
    printf("------------------------------------------------------\n");
    for (int i = 0; i < product_count; i++) {
        if (products[i].status == 1) {
            printf("%-5d %-15s %-10.2f %-10s %-10s\n",
                   products[i].product_id, products[i].name,
                   products[i].price, products[i].category,
                   products[i].pub_date);
        }
    }
}

void search_products() {
    char keyword[NAME_LEN];
    printf("请输入搜索关键词: ");
    scanf("%s", keyword);
    printf("\n===== 搜索结果 =====\n");
    int found = 0;
    for (int i = 0; i < product_count; i++) {
        if (products[i].status == 1 &&
            (strstr(products[i].name, keyword) ||
             strstr(products[i].category, keyword))) {
            printf("ID:%d 名称:%s 价格:%.2f 分类:%s\n",
                   products[i].product_id, products[i].name,
                   products[i].price, products[i].category);
            found++;
        }
    }
    if (!found) printf("未找到相关商品。\n");
}

void product_menu() {
    int choice;
    do {
        clear_screen();
        printf("\n===== 商品管理 =====\n");
        printf("1. 发布商品\n");
        printf("2. 浏览商品\n");
        printf("3. 搜索商品\n");
        printf("4. 修改商品\n");
        printf("5. 下架商品\n");
        printf("0. 返回主菜单\n");
        printf("请选择: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: publish_product(); break;
            case 2: browse_products(); break;
            case 3: search_products(); break;
            case 4: {
                int pid;
                printf("请输入商品ID: ");
                scanf("%d", &pid);
                if (pid > 0 && pid <= product_count) {
                    printf("请输入新价格: ");
                    scanf("%f", &products[pid-1].price);
                    save_products();
                    printf("修改成功！\n");
                }
                break;
            }
            case 5: {
                int pid;
                printf("请输入要下架的商品ID: ");
                scanf("%d", &pid);
                if (pid > 0 && pid <= product_count) {
                    products[pid-1].status = 0;
                    save_products();
                    printf("下架成功！\n");
                }
                break;
            }
        }
        if (choice != 0) pause_screen();
    } while (choice != 0);
}

/* ========== 订单管理模块 ========== */
void create_order() {
    if (current_user_id <= 0) { printf("请先登录！\n"); return; }
    if (order_count >= MAX_ORDERS) { printf("订单数量已满！\n"); return; }
    int pid;
    printf("请输入要购买的商品ID: ");
    scanf("%d", &pid);
    if (pid <= 0 || pid > product_count || products[pid-1].status != 1) {
        printf("商品不存在或已下架！\n");
        return;
    }
    Order o;
    o.order_id = order_count + 1;
    o.buyer_id = current_user_id;
    o.product_id = pid;
    o.price = products[pid-1].price;
    o.status = 0;
    get_current_date(o.order_date);
    strcpy(o.complete_date, "");
    orders[order_count++] = o;
    products[pid-1].status = 2;
    save_orders();
    save_products();
    printf("下单成功！订单ID: %d 金额: %.2f\n", o.order_id, o.price);
}

void view_orders() {
    if (current_user_id <= 0) { printf("请先登录！\n"); return; }
    printf("\n===== 我的订单 =====\n");
    char *status_str[] = {"待付款", "已付款", "已完成", "已取消"};
    for (int i = 0; i < order_count; i++) {
        if (orders[i].buyer_id == current_user_id) {
            printf("订单ID:%d 商品:%s 金额:%.2f 状态:%s 日期:%s\n",
                   orders[i].order_id,
                   products[orders[i].product_id-1].name,
                   orders[i].price,
                   status_str[orders[i].status],
                   orders[i].order_date);
        }
    }
}

void order_menu() {
    int choice;
    do {
        clear_screen();
        printf("\n===== 订单管理 =====\n");
        printf("1. 下单购买\n");
        printf("2. 查看订单\n");
        printf("3. 确认付款\n");
        printf("4. 确认收货\n");
        printf("5. 取消订单\n");
        printf("0. 返回主菜单\n");
        printf("请选择: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: create_order(); break;
            case 2: view_orders(); break;
            case 3: {
                int oid;
                printf("请输入订单ID: ");
                scanf("%d", &oid);
                if (oid > 0 && oid <= order_count && orders[oid-1].status == 0) {
                    orders[oid-1].status = 1;
                    save_orders();
                    printf("付款成功！\n");
                } else printf("操作失败！\n");
                break;
            }
            case 4: {
                int oid;
                printf("请输入订单ID: ");
                scanf("%d", &oid);
                if (oid > 0 && oid <= order_count && orders[oid-1].status == 1) {
                    orders[oid-1].status = 2;
                    get_current_date(orders[oid-1].complete_date);
                    save_orders();
                    printf("收货确认成功！交易完成。\n");
                } else printf("操作失败！\n");
                break;
            }
            case 5: {
                int oid;
                printf("请输入订单ID: ");
                scanf("%d", &oid);
                if (oid > 0 && oid <= order_count && orders[oid-1].status == 0) {
                    orders[oid-1].status = 3;
                    products[orders[oid-1].product_id-1].status = 1;
                    save_orders();
                    save_products();
                    printf("订单已取消。\n");
                } else printf("操作失败！\n");
                break;
            }
        }
        if (choice != 0) pause_screen();
    } while (choice != 0);
}

/* ========== 交易管理模块 ========== */
void transaction_menu() {
    int choice;
    do {
        clear_screen();
        printf("\n===== 交易管理 =====\n");
        printf("1. 查看交易记录\n");
        printf("2. 交易统计\n");
        printf("0. 返回主菜单\n");
        printf("请选择: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1:
                printf("\n===== 已完成交易 =====\n");
                for (int i = 0; i < order_count; i++) {
                    if (orders[i].status == 2) {
                        printf("订单:%d 商品:%s 金额:%.2f 完成日期:%s\n",
                               orders[i].order_id,
                               products[orders[i].product_id-1].name,
                               orders[i].price,
                               orders[i].complete_date);
                    }
                }
                break;
            case 2: {
                float total = 0;
                int count = 0;
                for (int i = 0; i < order_count; i++) {
                    if (orders[i].status == 2) {
                        total += orders[i].price;
                        count++;
                    }
                }
                printf("\n交易统计:\n");
                printf("总交易笔数: %d\n", count);
                printf("总交易金额: %.2f元\n", total);
                printf("平均交易金额: %.2f元\n", count > 0 ? total/count : 0);
                break;
            }
        }
        if (choice != 0) pause_screen();
    } while (choice != 0);
}

/* ========== 系统管理模块 ========== */
void system_menu() {
    int choice;
    do {
        clear_screen();
        printf("\n===== 系统管理 =====\n");
        printf("1. 数据统计\n");
        printf("2. 用户列表\n");
        printf("3. 数据备份\n");
        printf("0. 返回主菜单\n");
        printf("请选择: ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: {
                printf("\n===== 系统数据统计 =====\n");
                printf("注册用户数: %d\n", user_count);
                printf("商品总数: %d\n", product_count);
                int on_sale = 0;
                for (int i = 0; i < product_count; i++)
                    if (products[i].status == 1) on_sale++;
                printf("在售商品数: %d\n", on_sale);
                printf("订单总数: %d\n", order_count);
                break;
            }
            case 2:
                printf("\n===== 用户列表 =====\n");
                for (int i = 0; i < user_count; i++) {
                    printf("ID:%d 用户名:%s 手机:%s 角色:%s\n",
                           users[i].user_id, users[i].username,
                           users[i].phone,
                           users[i].role == 2 ? "管理员" :
                           (users[i].role == 1 ? "卖家" : "买家"));
                }
                break;
            case 3:
                save_users();
                save_products();
                save_orders();
                printf("数据备份完成！\n");
                break;
        }
        if (choice != 0) pause_screen();
    } while (choice != 0);
}

/* ========== 主函数 ========== */
int main() {
    // 加载数据
    load_users();
    load_products();
    load_orders();

    // 初始化管理员账户
    if (user_count == 0) {
        strcpy(users[0].username, "admin");
        strcpy(users[0].password, "admin123");
        strcpy(users[0].phone, "10000000000");
        users[0].user_id = 1;
        users[0].role = 2;
        get_current_date(users[0].reg_date);
        user_count = 1;
        save_users();
    }

    int choice;
    do {
        clear_screen();
        printf("\n");
        printf("========================================\n");
        printf("||   转转二手交易管理系统 v1.0        ||\n");
        printf("========================================\n");
        printf("||   1. 用户管理                      ||\n");
        printf("||   2. 商品管理                      ||\n");
        printf("||   3. 订单管理                      ||\n");
        printf("||   4. 交易管理                      ||\n");
        printf("||   5. 系统管理                      ||\n");
        printf("||   0. 退出系统                      ||\n");
        printf("========================================\n");
        if (current_user_id > 0)
            printf("当前用户: %s\n", users[current_user_id-1].username);
        printf("请输入功能编号(0-5): ");
        scanf("%d", &choice);
        switch (choice) {
            case 1: user_menu(); break;
            case 2: product_menu(); break;
            case 3: order_menu(); break;
            case 4: transaction_menu(); break;
            case 5: system_menu(); break;
            case 0:
                save_users();
                save_products();
                save_orders();
                printf("感谢使用，再见！\n");
                break;
            default: printf("无效选择！\n"); break;
        }
    } while (choice != 0);

    return 0;
}
