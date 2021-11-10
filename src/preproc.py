import string
import warnings

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, StandardScaler


warnings.filterwarnings("ignore")


def concat_df(train_data, test_data):
    # Returns a concatenated df of training and test set
    return pd.concat([train_data, test_data], sort=True).reset_index(drop=True)


def divide_df(all_data):
    # Returns divided dfs of training and test set
    return all_data.loc[:890], all_data.loc[891:].drop(["Survived"], axis=1)


df_train = pd.read_csv("../data/raw/train.csv")
df_test = pd.read_csv("../data/raw/test.csv")
df_all = concat_df(df_train, df_test)

df_train.name = "Training Set"
df_test.name = "Test Set"
df_all.name = "All Set"

dfs = [df_train, df_test]

print("Number of Training Examples = {}".format(df_train.shape[0]))
print("Number of Test Examples = {}\n".format(df_test.shape[0]))
print("Training X Shape = {}".format(df_train.shape))
print("Training y Shape = {}\n".format(df_train["Survived"].shape[0]))
print("Test X Shape = {}".format(df_test.shape))
print("Test y Shape = {}\n".format(df_test.shape[0]))
print(df_train.columns)
print(df_test.columns)


def display_missing(df):
    for col in df.columns.tolist():
        print("{} column missing values: {}".format(col, df[col].isnull().sum()))
    print("\n")


for df in dfs:
    print("{}".format(df.name))
    display_missing(df)

df_all_corr = (
    df_all.corr().abs().unstack().sort_values(kind="quicksort", ascending=False).reset_index()
)
df_all_corr.rename(
    columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: "Correlation Coefficient"},
    inplace=True,
)

age_by_pclass_sex = df_all.groupby(["Sex", "Pclass"]).median()["Age"]

for pclass in range(1, 4):
    for sex in ["female", "male"]:
        print("Median age of Pclass {} {}s: {}".format(pclass, sex, age_by_pclass_sex[sex][pclass]))
print("Median age of all passengers: {}".format(df_all["Age"].median()))

# Filling the missing values in Age with the medians of Sex and Pclass groups
df_all["Age"] = df_all.groupby(["Sex", "Pclass"])["Age"].apply(lambda x: x.fillna(x.median()))

df_all["Embarked"] = df_all["Embarked"].fillna("S")

med_fare = df_all.groupby(["Pclass", "Parch", "SibSp"]).Fare.median()[3][0][0]
# Filling the missing value in Fare with the median Fare of 3rd class alone passenger
df_all["Fare"] = df_all["Fare"].fillna(med_fare)

# Creating Deck column from the first letter of the Cabin column (M stands for Missing)
df_all["Deck"] = df_all["Cabin"].apply(lambda s: s[0] if pd.notnull(s) else "M")

df_all_decks = (
    df_all.groupby(["Deck", "Pclass"])
    .count()
    .drop(
        columns=[
            "Survived",
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Fare",
            "Embarked",
            "Cabin",
            "PassengerId",
            "Ticket",
        ]
    )
    .rename(columns={"Name": "Count"})
    .transpose()
)


def get_pclass_dist(df):

    # Creating a dictionary for every passenger class count in every deck
    deck_counts = {"A": {}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}, "G": {}, "M": {}, "T": {}}
    decks = df.columns.levels[0]

    for deck in decks:
        for pclass in range(1, 4):
            try:
                count = df[deck][pclass][0]
                deck_counts[deck][pclass] = count
            except KeyError:
                deck_counts[deck][pclass] = 0

    df_decks = pd.DataFrame(deck_counts)
    deck_percentages = {}

    # Creating a dictionary for every passenger class percentage in every deck
    for col in df_decks.columns:
        deck_percentages[col] = [(count / df_decks[col].sum()) * 100 for count in df_decks[col]]

    return deck_counts, deck_percentages


def display_pclass_dist(percentages):

    df_percentages = pd.DataFrame(percentages).transpose()
    deck_names = ("A", "B", "C", "D", "E", "F", "G", "M", "T")
    bar_count = np.arange(len(deck_names))
    bar_width = 0.85

    pclass1 = df_percentages[0]
    pclass2 = df_percentages[1]
    pclass3 = df_percentages[2]

    plt.figure(figsize=(20, 10))
    plt.bar(
        bar_count,
        pclass1,
        color="#b5ffb9",
        edgecolor="white",
        width=bar_width,
        label="Passenger Class 1",
    )
    plt.bar(
        bar_count,
        pclass2,
        bottom=pclass1,
        color="#f9bc86",
        edgecolor="white",
        width=bar_width,
        label="Passenger Class 2",
    )
    plt.bar(
        bar_count,
        pclass3,
        bottom=pclass1 + pclass2,
        color="#a3acff",
        edgecolor="white",
        width=bar_width,
        label="Passenger Class 3",
    )

    plt.xlabel("Deck", size=15, labelpad=20)
    plt.ylabel("Passenger Class Percentage", size=15, labelpad=20)
    plt.xticks(bar_count, deck_names)
    plt.tick_params(axis="x", labelsize=15)
    plt.tick_params(axis="y", labelsize=15)

    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), prop={"size": 15})
    plt.title("Passenger Class Distribution in Decks", size=18, y=1.05)

    plt.show()


all_deck_count, all_deck_per = get_pclass_dist(df_all_decks)
display_pclass_dist(all_deck_per)

idx = df_all[df_all["Deck"] == "T"].index
df_all.loc[idx, "Deck"] = "A"

df_all_decks_survived = (
    df_all.groupby(["Deck", "Survived"])
    .count()
    .drop(
        columns=[
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Fare",
            "Embarked",
            "Pclass",
            "Cabin",
            "PassengerId",
            "Ticket",
        ]
    )
    .rename(columns={"Name": "Count"})
    .transpose()
)


def get_survived_dist(df):

    # Creating a dictionary for every survival count in every deck
    surv_counts = {"A": {}, "B": {}, "C": {}, "D": {}, "E": {}, "F": {}, "G": {}, "M": {}}
    decks = df.columns.levels[0]

    for deck in decks:
        for survive in range(0, 2):
            surv_counts[deck][survive] = df[deck][survive][0]

    df_surv = pd.DataFrame(surv_counts)
    surv_percentages = {}

    for col in df_surv.columns:
        surv_percentages[col] = [(count / df_surv[col].sum()) * 100 for count in df_surv[col]]

    return surv_counts, surv_percentages


def display_surv_dist(percentages):

    df_survived_percentages = pd.DataFrame(percentages).transpose()
    deck_names = ("A", "B", "C", "D", "E", "F", "G", "M")
    bar_count = np.arange(len(deck_names))
    bar_width = 0.85

    not_survived = df_survived_percentages[0]
    survived = df_survived_percentages[1]

    plt.figure(figsize=(20, 10))
    plt.bar(
        bar_count,
        not_survived,
        color="#b5ffb9",
        edgecolor="white",
        width=bar_width,
        label="Not Survived",
    )
    plt.bar(
        bar_count,
        survived,
        bottom=not_survived,
        color="#f9bc86",
        edgecolor="white",
        width=bar_width,
        label="Survived",
    )

    plt.xlabel("Deck", size=15, labelpad=20)
    plt.ylabel("Survival Percentage", size=15, labelpad=20)
    plt.xticks(bar_count, deck_names)
    plt.tick_params(axis="x", labelsize=15)
    plt.tick_params(axis="y", labelsize=15)

    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), prop={"size": 15})
    plt.title("Survival Percentage in Decks", size=18, y=1.05)

    plt.show()


all_surv_count, all_surv_per = get_survived_dist(df_all_decks_survived)

df_all["Deck"] = df_all["Deck"].replace(["A", "B", "C"], "ABC")
df_all["Deck"] = df_all["Deck"].replace(["D", "E"], "DE")
df_all["Deck"] = df_all["Deck"].replace(["F", "G"], "FG")

df_all["Deck"].value_counts()

df_all.drop(["Cabin"], inplace=True, axis=1)

df_train, df_test = divide_df(df_all)
dfs = [df_train, df_test]


df_train_corr = (
    df_train.drop(["PassengerId"], axis=1)
    .corr()
    .abs()
    .unstack()
    .sort_values(kind="quicksort", ascending=False)
    .reset_index()
)
df_train_corr.rename(
    columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: "Correlation Coefficient"},
    inplace=True,
)
df_train_corr.drop(df_train_corr.iloc[1::2].index, inplace=True)
df_train_corr_nd = df_train_corr.drop(
    df_train_corr[df_train_corr["Correlation Coefficient"] == 1.0].index
)

df_test_corr = (
    df_test.corr().abs().unstack().sort_values(kind="quicksort", ascending=False).reset_index()
)
df_test_corr.rename(
    columns={"level_0": "Feature 1", "level_1": "Feature 2", 0: "Correlation Coefficient"},
    inplace=True,
)
df_test_corr.drop(df_test_corr.iloc[1::2].index, inplace=True)
df_test_corr_nd = df_test_corr.drop(
    df_test_corr[df_test_corr["Correlation Coefficient"] == 1.0].index
)

cat_features = ["Embarked", "Parch", "Pclass", "Sex", "SibSp", "Deck"]

df_all = concat_df(df_train, df_test)

df_all["Fare"] = pd.qcut(df_all["Fare"], 13)

df_all["Family_Size"] = df_all["SibSp"] + df_all["Parch"] + 1
family_map = {
    1: "Alone",
    2: "Small",
    3: "Small",
    4: "Small",
    5: "Medium",
    6: "Medium",
    7: "Large",
    8: "Large",
    11: "Large",
}
df_all["Family_Size_Grouped"] = df_all["Family_Size"].map(family_map)
df_all["Ticket_Frequency"] = df_all.groupby("Ticket")["Ticket"].transform("count")
df_all["Title"] = df_all["Name"].str.split(", ", expand=True)[1].str.split(".", expand=True)[0]
df_all["Is_Married"] = 0
df_all["Is_Married"].loc[df_all["Title"] == "Mrs"] = 1


def extract_surname(data):

    families = []

    for i in range(len(data)):
        name = data.iloc[i]

        if "(" in name:
            name_no_bracket = name.split("(")[0]
        else:
            name_no_bracket = name

        family = name_no_bracket.split(",")[0]
        title = name_no_bracket.split(",")[1].strip().split(" ")[0]

        for c in string.punctuation:
            family = family.replace(c, "").strip()

        families.append(family)

    return families


df_all["Family"] = extract_surname(df_all["Name"])
df_train = df_all.loc[:890]
df_test = df_all.loc[891:]
dfs = [df_train, df_test]

non_unique_families = [x for x in df_train["Family"].unique() if x in df_test["Family"].unique()]
non_unique_tickets = [x for x in df_train["Ticket"].unique() if x in df_test["Ticket"].unique()]

df_family_survival_rate = df_train.groupby("Family")["Survived", "Family", "Family_Size"].median()
df_ticket_survival_rate = df_train.groupby("Ticket")[
    "Survived", "Ticket", "Ticket_Frequency"
].median()

family_rates = {}
ticket_rates = {}

for i in range(len(df_family_survival_rate)):
    # Checking a family exists in both training and test set, and has members more than 1
    if (
        df_family_survival_rate.index[i] in non_unique_families
        and df_family_survival_rate.iloc[i, 1] > 1
    ):
        family_rates[df_family_survival_rate.index[i]] = df_family_survival_rate.iloc[i, 0]

for i in range(len(df_ticket_survival_rate)):
    # Checking a ticket exists in both training and test set, and has members more than 1
    if (
        df_ticket_survival_rate.index[i] in non_unique_tickets
        and df_ticket_survival_rate.iloc[i, 1] > 1
    ):
        ticket_rates[df_ticket_survival_rate.index[i]] = df_ticket_survival_rate.iloc[i, 0]


mean_survival_rate = np.mean(df_train["Survived"])

train_family_survival_rate = []
train_family_survival_rate_NA = []
test_family_survival_rate = []
test_family_survival_rate_NA = []

for i in range(len(df_train)):
    if df_train["Family"][i] in family_rates:
        train_family_survival_rate.append(family_rates[df_train["Family"][i]])
        train_family_survival_rate_NA.append(1)
    else:
        train_family_survival_rate.append(mean_survival_rate)
        train_family_survival_rate_NA.append(0)

for i in range(len(df_test)):
    if df_test["Family"].iloc[i] in family_rates:
        test_family_survival_rate.append(family_rates[df_test["Family"].iloc[i]])
        test_family_survival_rate_NA.append(1)
    else:
        test_family_survival_rate.append(mean_survival_rate)
        test_family_survival_rate_NA.append(0)

df_train["Family_Survival_Rate"] = train_family_survival_rate
df_train["Family_Survival_Rate_NA"] = train_family_survival_rate_NA
df_test["Family_Survival_Rate"] = test_family_survival_rate
df_test["Family_Survival_Rate_NA"] = test_family_survival_rate_NA

train_ticket_survival_rate = []
train_ticket_survival_rate_NA = []
test_ticket_survival_rate = []
test_ticket_survival_rate_NA = []

for i in range(len(df_train)):
    if df_train["Ticket"][i] in ticket_rates:
        train_ticket_survival_rate.append(ticket_rates[df_train["Ticket"][i]])
        train_ticket_survival_rate_NA.append(1)
    else:
        train_ticket_survival_rate.append(mean_survival_rate)
        train_ticket_survival_rate_NA.append(0)

for i in range(len(df_test)):
    if df_test["Ticket"].iloc[i] in ticket_rates:
        test_ticket_survival_rate.append(ticket_rates[df_test["Ticket"].iloc[i]])
        test_ticket_survival_rate_NA.append(1)
    else:
        test_ticket_survival_rate.append(mean_survival_rate)
        test_ticket_survival_rate_NA.append(0)

df_train["Ticket_Survival_Rate"] = train_ticket_survival_rate
df_train["Ticket_Survival_Rate_NA"] = train_ticket_survival_rate_NA
df_test["Ticket_Survival_Rate"] = test_ticket_survival_rate
df_test["Ticket_Survival_Rate_NA"] = test_ticket_survival_rate_NA


for df in [df_train, df_test]:
    df["Survival_Rate"] = (df["Ticket_Survival_Rate"] + df["Family_Survival_Rate"]) / 2
    df["Survival_Rate_NA"] = (df["Ticket_Survival_Rate_NA"] + df["Family_Survival_Rate_NA"]) / 2

non_numeric_features = ["Embarked", "Sex", "Deck", "Title", "Family_Size_Grouped", "Age", "Fare"]

for df in dfs:
    for feature in non_numeric_features:
        df[feature] = LabelEncoder().fit_transform(df[feature])

cat_features = ["Pclass", "Sex", "Deck", "Embarked", "Title", "Family_Size_Grouped"]
encoded_features = []

for df in dfs:
    for feature in cat_features:
        encoded_feat = OneHotEncoder().fit_transform(df[feature].values.reshape(-1, 1)).toarray()
        n = df[feature].nunique()
        cols = ["{}_{}".format(feature, n) for n in range(1, n + 1)]
        encoded_df = pd.DataFrame(encoded_feat, columns=cols)
        encoded_df.index = df.index
        encoded_features.append(encoded_df)

df_train = pd.concat([df_train, *encoded_features[:6]], axis=1)
df_test = pd.concat([df_test, *encoded_features[6:]], axis=1)

df_all = concat_df(df_train, df_test)
drop_cols = [
    "Deck",
    "Embarked",
    "Family",
    "Family_Size",
    "Family_Size_Grouped",
    "Survived",
    "Name",
    "Parch",
    "PassengerId",
    "Pclass",
    "Sex",
    "SibSp",
    "Ticket",
    "Title",
    "Ticket_Survival_Rate",
    "Family_Survival_Rate",
    "Ticket_Survival_Rate_NA",
    "Family_Survival_Rate_NA",
]

df_all.drop(columns=drop_cols, inplace=True)

X_train = StandardScaler().fit_transform(df_train.drop(columns=drop_cols))
y_train = df_train["Survived"].values
X_test = StandardScaler().fit_transform(df_test.drop(columns=drop_cols))


print("X_train shape: {}".format(X_train.shape))
print("y_train shape: {}".format(y_train.shape))
print("X_test shape: {}".format(X_test.shape))
pd.DataFrame(X_train).to_csv("../data/processed/X_train.csv")
pd.DataFrame(X_test).to_csv("../data/processed/X_test.csv")
pd.DataFrame(y_train).to_csv("../data/processed/y_train.csv")
df_test.to_csv("../data/processed/df_test.csv")
df_all.to_csv("../data/processed/df_all.csv")
