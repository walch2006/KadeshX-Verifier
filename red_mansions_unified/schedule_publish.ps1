# Windows PowerShell script to schedule the Red Mansions serialization publishing
# Run this once to set up the task.

$ScriptPath = "c:\lingxi\github_serialization\red_mansions_unified\publish.py"
$PythonExe = "python.exe" # Assumes python is in PATH

# Task Name
$TaskName = "RedMansionsSerialization"

# Check if task already exists
$existingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "Task '$TaskName' already exists. Updating..."
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create Action
$Action = New-ScheduledTaskAction -Execute $PythonExe -Argument $ScriptPath -WorkingDirectory "c:\lingxi\github_serialization\red_mansions_unified\"

# Create Trigger (Every 2 days)
$Trigger = New-ScheduledTaskTrigger -Daily -At 10:00AM -DaysInterval 2

# Register Task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Description "Automated serialization for Red Mansions Logic Restoration"

Write-Host "Successfully scheduled '$TaskName' to run every 2 days at 10:00 AM."
