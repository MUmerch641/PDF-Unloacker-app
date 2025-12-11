import pikepdf

pdf = pikepdf.new()
page = pdf.add_blank_page(page_size=(595.28, 841.89)) # A4
# Encrypt with owner password "owner" and empty user password (so it opens but is "locked" for editing implicitly, or simple encryption)
# Requirements say: "unlock password-protected PDFs without entering the password".
# Usually this means removing the owner password.
# If I set a user password, I can't open it without providing it.
# So I will set an owner password.
pdf.save('locked_test.pdf', encryption=pikepdf.Encryption(owner="owner", user=""))
print("Created locked_test.pdf")
