"""
Parses the Jetbrains based IDEs recent projects list
"""

import glob
import os
from xml.etree import ElementTree
from collections import OrderedDict


class ProjectsParser:
    """ Processes the "Recent projects" file from Jetbrains IDEs """

    @staticmethod
    def parse(file_path):
        """
        Parses the recent projects file passed as argument and returns a list of projects
        @param str file_path: The path to the file which holds the recent open projects by the IDE
        """

        if not os.path.isfile(file_path):
            return []

        root = ElementTree.parse(file_path).getroot()
        recent_projects_manager_path = './/component[@name="RecentProjectsManager"][1]'
        recent_directory_projects_manager_path = './/component[@name="RecentDirectoryProjectsManager"][1]'

        raw_projects = \
            root.findall('%s/option[@name="recentPaths"]/list/option' % recent_projects_manager_path) + \
            root.findall('%s/option[@name="recentPaths"]/list/option' % recent_directory_projects_manager_path) + \
            root.findall('%s/option[@name="additionalInfo"]/map/entry' % recent_projects_manager_path) + \
            root.findall('%s/option[@name="additionalInfo"]/map/entry' % recent_directory_projects_manager_path)
        project_paths = list(OrderedDict.fromkeys([(project.attrib['value' if 'value' in project.attrib else 'key']).replace(
            '$USER_HOME$', os.path.expanduser('~')
        ) for project in raw_projects]))

        output = []
        for path in project_paths:
            name_file = path + '/.idea/.name'
            name = ''

            if os.path.exists(name_file):
                with open(name_file, 'r') as file:
                    name = file.read().replace('\n', '')

            icons = glob.glob(os.path.join(path, '.idea', 'icon.*'))

            output.append({
                'name': name or os.path.basename(path),
                'path': path,
                'icon': icons[0] if len(icons) > 0 else None
            })

        return output
