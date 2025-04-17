# ans2dev\.general collection Release Notes

**Topics**

- <a href="#v0-2-0">v0\.2\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#minor-changes">Minor Changes</a>
    - <a href="#new-modules">New Modules</a>
- <a href="#v0-1-0">v0\.1\.0</a>
    - <a href="#release-summary-1">Release Summary</a>
    - <a href="#new-modules-1">New Modules</a>

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary"></a>
### Release Summary

New release of the <code>ans2dev\.general</code> collection\.
The changelog describes all changes made to the modules and plugins included in this collection\.
Official documentation is now avaible at [https\://3a2dev\.github\.io/ans2dev\.general](https\://3a2dev\.github\.io/ans2dev\.general)

<a id="minor-changes"></a>
### Minor Changes

* open\_xl \- add new <code>n</code> value for <code>op</code> option to create new excel file without <code>src</code> \([https\://github\.com/3A2DEV/ans2dev\.general/pull/116](https\://github\.com/3A2DEV/ans2dev\.general/pull/116)\)\.
* open\_xl \- fix <code>bgColor</code> format cells when write data\, now module reapply the format \([https\://github\.com/3A2DEV/ans2dev\.general/pull/142](https\://github\.com/3A2DEV/ans2dev\.general/pull/142)\)\.
* sar\_facts \- Updated to follow the Ansible standard\, it now uses <code>module\.run\_command\(\)</code> and <code>module\.get\_bin\_path\(\)</code> \([https\://github\.com/3A2DEV/ans2dev\.general/pull/154](https\://github\.com/3A2DEV/ans2dev\.general/pull/154)\)\.

<a id="new-modules"></a>
### New Modules

* ans2dev\.general\.chrony\_info \- Collect chrony information\.
* ans2dev\.general\.udevadm\_control \- Reload udev rules\.
* ans2dev\.general\.udevadm\_info \- Collect udevadm device information\.
* ans2dev\.general\.udevadm\_trigger \- Trigger udev rules\.
* ans2dev\.general\.udevadm\_verify \- Verify udev rules file\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-1"></a>
### Release Summary

This is the first proper release of the <code>ans2dev\.general</code> collection\.
The changelog describes all changes made to the modules and plugins included in this collection\.

<a id="new-modules-1"></a>
### New Modules

* ans2dev\.general\.charts \- Generate high\-quality charts using Plotly and save them as images\.
* ans2dev\.general\.exa\_facts \- Gathers facts about Oracle Exadata Machine and rack\.
* ans2dev\.general\.open\_xl \- Read and update Excel files using openpyxl\.
* ans2dev\.general\.sar\_facts \- Collect system activity report \(SAR\) data for system performance monitoring\.
