from core.promotion import Promoter
from core.providers import JiraBoardProvider, MunkiRepoProvider

if __name__ == "__main__":
    __j = JiraBoardProvider("test1")
    __j.load()
    __m = MunkiRepoProvider("test1")
    __m.load()

    promoter = Promoter(__m.get(), __j.get())

    promoter.promote()

    __j._packages_dict.update(promoter.jira_pkgs)

    __j.update_jira_from_repo(__m.get())

    __j.commit()

    print()
