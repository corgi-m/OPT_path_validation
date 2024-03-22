from tools.tools import strcat


class PPVHelper:
    @staticmethod
    def packet_info(PATH):
        src = PATH[0]
        srcp = PATH[0]
        dst = PATH[-1]
        dstp = PATH[-1]
        prtl = 'PPV'

        return src, srcp, dst, dstp, prtl

    @staticmethod
    def verify_info(add, package, index, PATH, flowid, src):
        TTL1 = package.PPV_get_TTL() + index - PATH.index(add)
        Rid1_ = PATH[PATH.index(add) - 1]
        return strcat(src, TTL1, Rid1_, flowid)
