from elftools.dwarf.descriptions import describe_reg_name

class FDE():
    """
    Represent a fde entry with the table already calculated during load time

    :param low_pc:      under bound of program counter (inclusive)
    :param high_pc:     upper bound of program connter (exclusive)
    :param table:       table to calculate cfa
    """

    def __init__(self, low_pc: int, high_pc: int, table: List[CFARule]):
        self.low_pc = low_pc
        self.high_pc = high_pc
        self.table = table

    @staticmethod
    def load_fde(fde, arch):
        """
        Entry method to read a elftools.dwarf.callframe.FDE from pyelftools
        """
        low_pc = fde.header.initial_location
        high_pc = low_pc + fde.header.address_range
        decode_table = fde.get_decoded().table
        table = []
        for index, entry in enumerate(decode_table):
            rule_low_pc = entry['pc']
            if index == len(decode_table) - 1:
                rule_high_pc = high_pc
            else:
                rule_high_pc = decode_table[index + 1]['pc']
            regnum = entry['cfa'].reg
            reg = describe_reg_name(regnum, arch) if regnum is not None else None
            offset = entry['cfa'].offset
            expr = entry['cfa'].expr
            rule = CFARule(rule_low_pc, rule_high_pc, reg, offset, expr)
            table.append(rule)
        return FDE(low_pc, high_pc, table)


class CFARule():
    """
    Represent a rule to compute cfa from dwarf call frame

    :param low_pc:      under bound of program counter (inclusive)
    :param high_pc:     upper bound of program connter (exclusive)
    :param reg:         reference register to calculate cfa from
    :param offset:      offset from the reference register
    :param expr:        List of expr to calculate cfa when it is not reference from register
    """

    def __init__(self, low_pc:int, high_pc:int, reg: str, offset: int, expr):
        self.low_pc = low_pc
        self.high_pc = high_pc
        self.reg = reg
        self.offset = offset
        self.expr = expr


