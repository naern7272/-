class FixedExpense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __str__(self):
        return f"{self.name} ({self.category}) : {self.amount:,}원"

class FixedExpenseManager:
    def __init__(self):
        self.fixed_expenses = []

    # 고정지출 추가
    def add_expense(self, name, category, amount):
        if amount < 0:
            raise ValueError("금액은 음수일 수 없습니다.")

        expense = FixedExpense(name, category, amount)
        self.fixed_expenses.append(expense)

    # 고정지출 삭제
    def remove_expense(self, name):
        for expense in self.fixed_expenses:
            if expense.name == name:
                self.fixed_expenses.remove(expense)
                return True
        return False

    # 고정지출 수정
    def update_expense(self, name, new_amount):
        if new_amount < 0:
            raise ValueError("금액은 음수일 수 없습니다.")

        for expense in self.fixed_expenses:
            if expense.name == name:
                expense.amount = new_amount
                return True
        return False

    # 고정지출 목록 조회
    def show_expenses(self):
        for expense in self.fixed_expenses:
            print(expense)

    # 고정지출 총합 계산
    def get_total_expense(self):
        return sum(
            expense.amount
            for expense in self.fixed_expenses
        )

class BudgetManager:
    def __init__(self, total_budget, fixed_manager):
        self.total_budget = total_budget
        self.fixed_manager = fixed_manager

        # 카테고리별 예산
        self.category_budgets = {}

        # 경고 관리자
        self.warning_manager = BudgetWarningManager()

    # 카테고리별 예산 설정
    def set_category_budget(self, category, amount):
        if amount < 0:
            raise ValueError("예산은 음수일 수 없습니다.")

        self.category_budgets[category] = amount

    # 전체 사용 가능 예산
    def get_available_budget(self):
        available = (
            self.total_budget
            - self.fixed_manager.get_total_expense()
        )

        if available < 0:
            raise ValueError("고정지출이 전체 예산을 초과했습니다.")

        return available

    # 전체 일반 소비 합계
    def get_total_used(self, expenses):
        return sum(e.amount for e in expenses)

    # 카테고리별 소비 합계
    def get_category_used(self, expenses, category):
        return sum(
            e.amount for e in expenses
            if e.category == category
        )

    # 전체 남은 예산
    def get_remaining_budget(self, expenses):
        return (
            self.get_available_budget()
            - self.get_total_used(expenses)
        )

    # 카테고리별 남은 예산
    def get_category_remaining(self, expenses, category):
        budget = self.category_budgets.get(category, 0)
        used = self.get_category_used(expenses, category)

        return budget - used

    # 전체 예산 사용률
    def get_total_usage_rate(self, expenses):
        available = self.get_available_budget()

        if available == 0:
            return 0

        return self.get_total_used(expenses) / available * 100

    # 카테고리별 예산 사용률
    def get_category_usage_rate(self, expenses, category):
        budget = self.category_budgets.get(category, 0)

        if budget == 0:
            return 0

        used = self.get_category_used(expenses, category)

        return used / budget * 100

    # 전체 예산 경고
    def get_total_warning(self, expenses):
        rate = self.get_total_usage_rate(expenses)
        return self.warning_manager.check_warning(rate)

    # 카테고리별 예산 경고
    def get_category_warning(self, expenses, category):
        rate = self.get_category_usage_rate(expenses, category)
        return self.warning_manager.check_warning(rate)

    # 카테고리별 예산 현황 출력
    def show_category_budget(self, expenses):
        print("\n===== 카테고리별 예산 현황 =====")

        for category, budget in self.category_budgets.items():
            used = self.get_category_used(expenses, category)
            remaining = budget - used
            rate = self.get_category_usage_rate(expenses, category)

            print(f"\n[{category}]")
            print(f"설정 예산: {budget:,}원")
            print(f"현재 소비: {used:,}원")
            print(f"남은 예산: {remaining:,}원")
            print(f"사용률: {rate:.2f}%")
            print(f"상태: {self.get_category_warning(expenses, category)}")

    # 전체 예산 현황 출력
    def show_total_budget(self, expenses):
        available = self.get_available_budget()
        used = self.get_total_used(expenses)
        remaining = available - used
        rate = self.get_total_usage_rate(expenses)

        print("\n===== 전체 예산 현황 =====")
        print(f"전체 예산: {self.total_budget:,}원")
        print(f"고정지출: {self.fixed_manager.get_total_expense():,}원")
        print(f"사용 가능 예산: {available:,}원")
        print(f"현재 소비: {used:,}원")
        print(f"남은 예산: {remaining:,}원")
        print(f"사용률: {rate:.2f}%")
        print(f"상태: {self.get_total_warning(expenses)}")

class BudgetWarningManager:

    def check_warning(self, usage_rate):

        if usage_rate > 100:
            return "예산 초과! 지출을 줄여주세요."

        elif usage_rate >= 90:
            return "경고! 예산의 90% 이상 사용했습니다."

        elif usage_rate >= 75:
            return "경고! 예산의 75% 이상 사용했습니다."

        else:
            return "정상! 예산 범위 내입니다."