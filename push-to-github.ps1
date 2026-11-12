# Push this folder to https://github.com/gnana70/qwen4-max-preview-tests
# 1) Create the empty repo first on github.com/new (name: qwen4-max-preview-tests, Public, no README).
# 2) Run in PowerShell from this folder:  .\push-to-github.ps1
git remote remove origin 2>$null
git remote add origin https://github.com/gnana70/qwen4-max-preview-tests.git
git branch -M main
git push -u origin main
