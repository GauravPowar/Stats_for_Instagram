import os
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
import pandas as pd


def extract_usernames(html_path):
    with open(html_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
    return [a.text.strip() for a in soup.find_all('a', href=True) if "instagram.com" in a['href']]


def categorize_follow_data(followers_path, following_path, output_path="Instagram_Follow_Analysis.xlsx"):
    followers = set(extract_usernames(followers_path))
    following = set(extract_usernames(following_path))

    mutual = sorted(followers & following)
    followers_only = sorted(followers - following)
    following_only = sorted(following - followers)

    df = pd.DataFrame({
        "Mutual Follows": pd.Series(mutual),
        "Followers I Don’t Follow Back": pd.Series(followers_only),
        "Following Who Don’t Follow Me Back": pd.Series(following_only)
    })
    df.to_excel(output_path, index=False)
    return output_path


def select_file(entry_widget):
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])
    if file_path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, file_path)


def generate_excel():
    followers_path = entry_followers.get()
    following_path = entry_following.get()

    if not followers_path or not following_path:
        messagebox.showerror("Error", "Please select both files")
        return

    try:
        output_path = categorize_follow_data(followers_path, following_path)
        messagebox.showinfo("Success", f"Analysis saved to {output_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI Setup
root = tk.Tk()
root.title("Instagram Follow Analyzer")
root.geometry("500x200")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10, fill="x")

# Followers file
label_followers = tk.Label(frame, text="Followers HTML:")
label_followers.pack(anchor="w")
entry_followers = tk.Entry(frame, width=60)
entry_followers.pack(side="left", padx=5)
btn_browse_followers = tk.Button(frame, text="Browse", command=lambda: select_file(entry_followers))
btn_browse_followers.pack(side="right")

frame2 = tk.Frame(root)
frame2.pack(padx=10, pady=10, fill="x")

# Following file
label_following = tk.Label(frame2, text="Following HTML:")
label_following.pack(anchor="w")
entry_following = tk.Entry(frame2, width=60)
entry_following.pack(side="left", padx=5)
btn_browse_following = tk.Button(frame2, text="Browse", command=lambda: select_file(entry_following))
btn_browse_following.pack(side="right")

# Generate button
btn_generate = tk.Button(root, text="Generate Excel Report", command=generate_excel, bg="green", fg="white")
btn_generate.pack(pady=20)

root.mainloop()
