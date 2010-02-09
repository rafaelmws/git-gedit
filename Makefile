# Copyright Rafael Martins <rafael.mws@gmail.com>

# Licensed under the Open Software License ("OSL") v. 3.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.opensource.org/licenses/osl-3.0.php

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Makefile for Git-Gedit
SHELL := /bin/bash
pluginpath=~/.gnome2/gedit/plugins

install:
	@echo "-------- Initializing copies git-gedit ----------"
	@mkdir -r ${pluginpath}
	@cp -R ./git-gedit.gedit-plugin ${pluginpath}
	@cp -R ./git-gedit ${pluginpath}
	@echo "-------- Completed copies -----------"
