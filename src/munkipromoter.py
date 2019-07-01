from core.promotion import Promoter
from core.providers import JiraBoardProvider, MunkiRepoProvider

if __name__ == "__main__":
    __j = JiraBoardProvider("test1")
    __j.load()
    __m = MunkiRepoProvider("test1")
    __m.load()

    __j.update_jira_from_repo(__m.get())

    promoter = Promoter(__m.get(), __j.get())
    promoter.promote()

    for k, p in promoter.jira_pkgs.items():
        __j.update(p)
        __m.update(p)

    __j.commit()
    __m.commit()

    print()
