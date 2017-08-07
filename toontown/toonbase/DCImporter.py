from panda3d.core import *
dcString = """
from direct.distributed import DistributedObject/AI/UD
from direct.distributed import DistributedNode/AI/UD
from direct.distributed import DistributedSmoothNode/AI
from direct.distributed import DistributedCartesianGrid/AI
from direct.distributed import DistributedCamera/AI/OV
from otp.distributed import Account/AI/UD
from otp.ai import TimeManager/AI
from otp.ai import MagicWordManager/AI
from otp.avatar import DistributedAvatar/AI/UD
from otp.avatar import DistributedPlayer/AI
from otp.friends import FriendManager/AI
from otp.friends import AvatarFriendsManager/UD
from otp.friends import PlayerFriendsManager/UD
from otp.friends import GuildManager/AI/UD
from otp.friends import FriendInfo
from otp.friends import AvatarFriendInfo
from otp.distributed import ObjectServer/AI/UD
from otp.distributed import DistributedDistrict/AI/UD
from otp.distributed import DistributedDirectory/AI
from otp.distributed import DistributedTestObject/AI
from otp.snapshot import SnapshotDispatcher/AI/UD
from otp.snapshot import SnapshotRenderer/AI/UD
from otp.uberdog import OtpAvatarManager/AI/UD
from otp.chat import ChatAgent/AI/UD
from otp.uberdog import SpeedchatRelay/UD
from otp.distributed import CentralLogger/AI/UD
from otp.web import SettingsMgr/AI/UD
from otp.status import StatusDatabase/UD
from otp.avatar import AvatarHandle

typedef uint8 bool;

typedef uint32 DoId;

typedef DoId DoIdList[];

struct AvatarPendingDel {
  uint32 Avatar;
  uint32 date;
};

dclass Account {
  string DcObjectType db;
  uint32 ACCOUNT_AV_SET[] required db;
  uint32 ESTATE_ID db;
  AvatarPendingDel ACCOUNT_AV_SET_DEL[] db;
  string CREATED db;
  string LAST_LOGIN db;
  string ACCOUNT_ID db;
  uint16 ACCESS_LEVEL db;
  uint32 MONEY db;
  bool TYPE_CHAT_ALLOWED db;
};

struct BarrierData {
  uint16 context;
  string name;
  DoIdList avIds;
};

dclass DistributedObject {
  setBarrierData(BarrierData []) broadcast ram;
  setBarrierReady(uint16 barrierContext) airecv clsend;
  execCommand(string command, DoId magicWordMgr,
              DoId avatar, uint32 zoneId);
  broadcastMessage() broadcast;
};

dclass DistributedObjectGlobal : DistributedObject {
};

dclass DistributedTestObject : DistributedObject {
  uint32 AutoInterest[];
  setParentingRules(string, string) broadcast ram;
  setRequiredField(uint32) required broadcast ram;
  setB(uint32) broadcast;
  setBA(uint32) broadcast airecv;
  setBO(uint32) broadcast ownsend;
  setBR(uint32) broadcast ram;
  setBRA(uint32) broadcast ram airecv;
  setBRO(uint32) broadcast ram ownsend;
  setBROA(uint32) broadcast ram ownsend airecv;
};

struct OSInfo {
  string name;
  int16 platform;
  int16 major;
  int16 minor;
};

struct CPUSpeed {
  int32/1000 maxSpeed;
  int32/1000 currentSpeed;
};

dclass TimeManager : DistributedObject {
  requestServerTime(uint8 context) airecv clsend;
  serverTime(uint8 context, int32 timestap, uint32 timeOfDay);
  setDisconnectReason(uint8) airecv clsend;
  setExceptionInfo(string(0-1024)) airecv clsend;
  setSignature(string(0-1024) signature, char prcHash[16],
               char pycHash[16]) airecv clsend;
  setFrameRate(uint16/10 fps, uint16/1000 deviation, uint16 numAvatars,
               string(0-256) locationCode, uint32/10 timeInLocation,
               uint32/10 timeInGame, string(0-256) gameOptionsCode,
               uint16 vendorId, uint16 deviceId, uint32/10 processMemory,
               uint32/10 pageFileUsage, uint32/10 physicalMemory,
               uint32 pageFaultCount, OSInfo, CPUSpeed, uint16 cpuCores,
               uint16 logicalCPUs, string(0-256) apiName) airecv clsend;
  setCpuInfo(string(0-1024) infoStr, string cacheStatus) airecv clsend;
  checkForGarbageLeaks(bool) airecv clsend;
  setNumAIGarbageLeaks(uint32);
  setClientGarbageLeak(uint32, string(0-1024)) airecv clsend;
  checkAvOnDistrict(uint32 context, DoId avatar) clsend airecv;
  checkAvOnDistrictResult(uint32 context, DoId av, bool isOnDistrict);
};

dclass ObjectServer {
  setName(string) airecv ram required;
  setDcHash(uint32) ram required;
  setDateCreated(uint32) airecv;
};

dclass DistributedDirectory : DistributedObject {
  setParentingRules(string, string) broadcast ram;
};

dclass DistributedDistrict : DistributedObject {
  setName(string) required broadcast ram;
  setAvailable(uint8) required broadcast ram;
};

dclass DistributedNode : DistributedObject {
  setParentStr(blob) broadcast ram ownsend airecv;
  setParent(uint32) broadcast ram ownsend airecv;
  setX(int16/10) broadcast ram ownsend airecv;
  setY(int16/10) broadcast ram ownsend airecv;
  setZ(int16/10) broadcast ram ownsend airecv;
  setH(int16%360/10) broadcast ram ownsend airecv;
  setP(int16%360/10) broadcast ram ownsend airecv;
  setR(int16%360/10) broadcast ram ownsend airecv;
  setPos : setX, setY, setZ;
  setHpr : setH, setP, setR;
  setPosHpr : setX, setY, setZ, setH, setP, setR;
  setXY : setX, setY;
  setXZ : setX, setZ;
  setXYH : setX, setY, setH;
  setXYZH : setX, setY, setZ, setH;
};

dclass DistributedSmoothNode : DistributedNode {
  setComponentL(uint64) broadcast ram ownsend airecv;
  setComponentX(int16/10) broadcast ram ownsend airecv;
  setComponentY(int16/10) broadcast ram ownsend airecv;
  setComponentZ(int16/10) broadcast ram ownsend airecv;
  setComponentH(int16%360/10) broadcast ram ownsend airecv;
  setComponentP(int16%360/10) broadcast ram ownsend airecv;
  setComponentR(int16%360/10) broadcast ram ownsend airecv;
  setComponentT(int16) broadcast ram ownsend airecv;
  setSmStop : setComponentT;
  setSmH : setComponentH, setComponentT;
  setSmZ : setComponentZ, setComponentT;
  setSmXY : setComponentX, setComponentY, setComponentT;
  setSmXZ : setComponentX, setComponentZ, setComponentT;
  setSmPos : setComponentX, setComponentY, setComponentZ, setComponentT;
  setSmHpr : setComponentH, setComponentP, setComponentR, setComponentT;
  setSmXYH : setComponentX, setComponentY, setComponentH, setComponentT;
  setSmXYZH : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentT;
  setSmPosHpr : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  setSmPosHprL : setComponentL, setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  clearSmoothing(int8) broadcast ownsend;
  suggestResync(uint32, int16, int16, int32, uint16, uint16/100) ownrecv clsend;
  returnResync(uint32, int16, int32, uint16, uint16/100) ownrecv clsend;
};

dclass DistributedCartesianGrid : DistributedNode {
  setCellWidth(uint32) required broadcast ram;
  setParentingRules(string, string) broadcast ram;
};

struct Fixture {
  int32/10 x;
  int32/10 y;
  int32/10 z;
  int16/10 h;
  int16/10 p;
  int16/10 r;
  string state;
};

dclass DistributedCamera : DistributedNode {
  setCamParent(uint32) required broadcast ram ownsend airecv;
  setFixtures(Fixture []) required broadcast ram ownsend airecv;
};

struct TalkModification {
  uint16 offset;
  uint16 size;
};

dclass TalkPath_owner {
  setTalk(DoId fromAv, DoId fromAcc, string(0-256) avName,
          string(0-400) chat, TalkModification [], uint8 flags) broadcast ownsend;
};

dclass TalkPath_whisper {
  setTalkWhisper(DoId fromAv, DoId fromAcc, string(0-256) avName,
                 string(0-400) chat, TalkModification [], uint8 flags) ownrecv clsend;
};

dclass TalkPath_group {
  setTalkGroup(DoId fromAv, DoId fromAcc, string(0-256) avName,
               string(0-400) chat, TalkModification [], uint8 flags) clsend airecv;
};

dclass TalkPath_account {
  setTalkAccount(DoId toAcc, DoId fromAcc, string(0-256) avName,
                 string(0-400) msg, TalkModification [], uint8 flags) airecv clsend;
};

dclass AvatarHandle : TalkPath_whisper {
};

dclass DistributedAvatar : DistributedSmoothNode, TalkPath_whisper {
  string DcObjectType db;
  setName(string = "[Name not set]") required broadcast db airecv;
  setToonTag(string = "") required broadcast db airecv;
  friendsNotify(DoId avId, int8 status) ownrecv airecv;
  checkAvOnShard(DoId) clsend airecv;
  confirmAvOnShard(DoId avId, int8 isOnShard);
};

struct FriendEntry {
  uint32 friendId;
  uint8 friendType;
}

dclass DistributedPlayer : DistributedAvatar {
  arrivedOnDistrict(DoId districtId) ownrecv ram;
  setAccountName(string name = "") required ownrecv db;
  setWhisperSCFrom(DoId fromAv, uint16 msgIndex) ownrecv clsend;
  setWhisperSCCustomFrom(DoId fromAv, uint16 msgIndex) ownrecv clsend;
  setWhisperSCEmoteFrom(DoId fromAv, uint16 emoteId) ownrecv clsend;
  setSystemMessage(DoId aboutId, string(0-256) chatString) ownrecv;
  setCommonChatFlags(uint8) broadcast ownrecv ram airecv;
  setWhitelistChatFlags(uint8) broadcast ownrecv ram airecv;
  setSC(uint16 msgIndex) broadcast ownsend airecv;
  setSCCustom(uint16 msgIndex) broadcast ownsend airecv;
  setFriendsList(FriendEntry[] = []) ownrecv required db airecv;
  setDISLname(string) broadcast ownrecv ram;
  setDISLid(uint32 = 0) broadcast ownrecv ram db airecv required;
  setTalk(DoId fromAv, DoId fromAcc, string(0-256) avName,
          string(0-400) chat, TalkModification [], uint8 flags) broadcast ownsend;
  OwningAccount(DoId);
  WishName(string = "") db ram;
  WishNameState(string = "OPEN") db ram;
  setPreviousAccess(uint8 = 0) required db airecv;
  setAccess(uint8 = 2) broadcast ownrecv required ram airecv;
  setAdminAccess(uint16 = 0) broadcast ownrecv required airecv;
  setAsGM(bool = 0) required ram broadcast ownrecv airecv;
};

dclass MagicWordManager : DistributedObject {
  sendMagicWord(string, uint32) airecv clsend;
  sendMagicWordResponse(string);
};

dclass OtpAvatarManager : DistributedObject {
  online();
  requestAvatarList(uint32) airecv clsend;
  rejectAvatarList(uint32);
  avatarListResponse(blob);
  requestAvatarSlot(uint32, uint32, uint8) clsend airecv;
  rejectAvatarSlot(uint32, uint32, uint8);
  avatarSlotResponse(uint32, uint8);
  requestPlayAvatar(uint32, uint32, uint32) clsend airecv;
  rejectPlayAvatar(uint32, uint32);
  playAvatarResponse(uint32, uint32, uint8, uint8);
  rejectCreateAvatar(uint32);
  createAvatarResponse(uint32, uint32, uint8, uint8);
  requestRemoveAvatar(uint32, uint32, uint32, string(0-256)) airecv clsend;
  rejectRemoveAvatar(uint32);
  removeAvatarResponse(uint32, uint32);
  requestShareAvatar(uint32, uint32, uint32, uint8) airecv clsend;
  rejectShareAvatar(uint32);
  shareAvatarResponse(uint32, uint32, uint8);
};

dclass ChatAgent : DistributedObject {
  adminChat(uint32, string);
  chatMessage(string(0-256), uint8 chatMode) clsend;
  chatMessageAiToUd(uint32 avId, string(0-256), uint8 chatMode);
  chatMessageResponse(DoId, string, TalkModification [], uint8 chatMode) airecv;
  kickForSpam(uint32) airecv clsend;
};

dclass FriendManager : DistributedObject {
  friendQuery(int32) airecv clsend;
  cancelFriendQuery(int32) airecv clsend;
  inviteeFriendConsidering(int8, int32) airecv clsend;
  inviteeFriendResponse(int8, int32) airecv clsend;
  inviteeAcknowledgeCancel(int32) airecv clsend;
  friendConsidering(int8, int32);
  friendResponse(int8, int32);
  inviteeFriendQuery(int32, string, blob, int32);
  inviteeCancelFriendQuery(int32);
  requestSecret() airecv clsend;
  requestSecretResponse(int8, string);
  submitSecret(string(0-256)) airecv clsend;
  submitSecretResponse(int8, int32);
  requestTrueFriendCode() airecv clsend;
  useTrueFriendCode(string) airecv clsend;
  trueFriendResponse(uint8, string);
};

struct FriendInfo {
  string avatarName;
  uint32 avatarId;
  string playerName;
  uint8 onlineYesNo;
  uint8 openChatEnabledYesNo;
  uint8 openChatFriendshipYesNo;
  uint8 wlChatEnabledYesNo;
  string location;
  string sublocation;
  uint32 timestamp;
};

struct AvatarFriendInfo {
  string avatarName;
  string playerName;
  uint32 playerId;
  uint8 onlineYesNo;
  uint8 openChatEnabledYesNo;
  uint8 openChatFriendshipYesNo;
  uint8 wlChatEnabledYesNo;
};

struct MemberInfo {
  uint32 avatarId;
  string avatarName;
  uint8 avatarRank;
  uint8 avatarOnline;
  uint32 bandManagerId;
  uint32 bandId;
};

struct leaderBoardRecordResponces {
  char found;
  uint32 id;
  string text;
  int32 value;
};

struct leaderBoardRecord {
  uint32 id;
  string text;
  int32 value;
};

dclass LeaderBoardReceiver {
  getTopTenResponce(string, leaderBoardRecord []);
  getValuesResponce(string, leaderBoardRecordResponces []);
};

dclass LeaderBoard : LeaderBoardReceiver {
  setValue(string [], uint32, string, int32);
  alterValue(string [], uint32, string, int32);
  setHighScore(string [], uint32, string, int32);
  getValues(string, uint32 []);
  getTopTen(string);
  getValuesRespondTo(string, uint32 [], uint32);
  getTopTenRespondTo(string, uint32);
};

dclass GuildManager : DistributedObject, LeaderBoardReceiver, TalkPath_group {
  online();
  guildRejectInvite(uint32, uint32);
  invitationFrom(uint32, string, uint32, string);
  requestInvite(uint32) airecv clsend;
  memberList() airecv clsend;
  createGuild() airecv clsend;
  acceptInvite() airecv clsend;
  declineInvite() airecv clsend;
  setWantName(string(0-256)) airecv clsend;
  removeMember(uint32) airecv clsend;
  changeRank(uint32, uint8) airecv clsend;
  changeRankAvocate(uint32) airecv clsend;
  statusRequest() airecv clsend;
  requestLeaderboardTopTen() airecv clsend;
  guildStatusUpdate(uint32, string(0-256), uint8);
  guildNameReject(uint32);
  guildNameChange(string, uint8);
  receiveMember(MemberInfo);
  receiveMembersDone();
  guildAcceptInvite(uint32);
  guildDeclineInvite(uint32);
  updateRep(uint32, uint32);
  leaderboardTopTen(leaderBoardRecord []);
  recvAvatarOnline(uint32, string, uint32, uint32);
  recvAvatarOffline(uint32, string);
  sendChat(string(0-256), uint8, uint32) airecv clsend;
  sendWLChat(string(0-256), uint8, uint32) airecv clsend;
  sendSC(uint16) airecv clsend;
  sendSCQuest(uint16, uint16, uint16) airecv clsend;
  recvChat(uint32, string, uint8, uint32);
  recvWLChat(uint32, string, uint8, uint32);
  recvSC(uint32, uint16);
  recvSCQuest(uint32, uint16, uint16, uint16);
  sendTokenRequest() airecv clsend;
  recvTokenGenerated(string);
  recvTokenInviteValue(string, int8);
  sendTokenForJoinRequest(string(0-256), string(0-256)) airecv clsend;
  recvTokenRedeemMessage(string);
  recvTokenRedeemedByPlayerMessage(string);
  sendTokenRValue(string(0-256), int8) airecv clsend;
  sendPermToken() airecv clsend;
  sendNonPermTokenCount() airecv clsend;
  recvPermToken(string);
  recvNonPermTokenCount(uint8);
  sendClearTokens(uint8) airecv clsend;
  sendAvatarBandId(uint32, uint32, uint32);
  recvMemberAdded(MemberInfo, uint32, string);
  notifyGuildKicksMaxed();
  recvMemberRemoved(uint32, uint32, string, string);
  recvMemberUpdateName(uint32, string);
  recvMemberUpdateRank(uint32, uint32, string, string, uint8, bool);
  recvMemberUpdateBandId(uint32, uint32, uint32);
  avatarOnline(uint32, uint16);
  avatarOffline(uint32);
  reflectTeleportQuery(uint32, uint32, uint32, uint32, uint32) clsend airecv;
  teleportQuery(uint32, uint32, uint32, uint32, uint32);
  reflectTeleportResponse(uint32, int8, uint32, uint32, uint32) clsend airecv;
  teleportResponse(uint32, int8, uint32, uint32, uint32);
  requestGuildMatesList(uint32, uint32, uint32);
  updateAvatarName(uint32, string);
  avatarDeleted(uint32);
};

dclass AvatarFriendsManager : DistributedObject {
  online();
  requestInvite(uint32) airecv clsend;
  friendConsidering(uint32) airecv clsend;
  invitationFrom(uint32, string);
  retractInvite(uint32);
  rejectInvite(uint32, uint32);
  requestRemove(uint32) airecv clsend;
  rejectRemove(uint32, uint32);
  updateAvatarFriend(uint32, AvatarFriendInfo);
  removeAvatarFriend(uint32);
  updateAvatarName(uint32, string);
  avatarOnline(uint32, uint32, string, bool, bool, string, string);
  avatarOffline(uint32);
};

dclass PlayerFriendsManager : DistributedObject, TalkPath_account {
  requestInvite(uint32, uint32, uint8) airecv clsend;
  invitationFrom(uint32, string);
  retractInvite(uint32);
  invitationResponse(uint32, uint16, uint32);
  requestDecline(uint32, uint32) airecv clsend;
  requestDeclineWithReason(uint32, uint32, uint32) airecv clsend;
  requestRemove(uint32, uint32) airecv clsend;
  secretResponse(string);
  rejectSecret(string);
  rejectUseSecret(string);
  updatePlayerFriend(uint32, FriendInfo, uint8);
  removePlayerFriend(uint32);
};

dclass SnapshotDispatcher : DistributedObject {
  online();
  requestRender(uint32);
  avatarDeleted(uint32);
  requestNewWork(uint32);
  errorFetchingAvatar(uint32, uint32);
  errorRenderingAvatar(uint32, uint32);
  renderSuccessful(uint32, uint32);
};

dclass SnapshotRenderer : DistributedObject {
  online();
  requestRender(uint32, uint32, string);
};

dclass SpeedchatRelay : DistributedObject, TalkPath_account {
  forwardSpeedchat(uint32, uint8, uint32 [], uint32, string(0-256), uint8) clsend;
};

dclass CentralLogger : DistributedObject {
  sendMessage(string(0-256), string(0-1024), uint32, uint32) clsend;
  logAIGarbage() airecv;
};

dclass SettingsMgr : DistributedObject {
  requestAllChangedSettings() airecv clsend;
  settingChange(string, string) airecv;
};

dclass StatusDatabase : DistributedObject {
  requestOfflineAvatarStatus(uint32 []) airecv clsend;
  recvOfflineAvatarStatus(uint32, uint32);
};

dclass CallbackObject {
  callback(uint32, bool, uint8);
};

from direct.distributed import DistributedObjectGlobal
from toontown.ai import WelcomeValleyManager/AI
from toontown.building import DistributedAnimatedProp/AI
from toontown.toon import DistributedToon/AI/UD
from toontown.classicchars import DistributedCCharBase/AI
from toontown.classicchars import DistributedMickey/AI
from toontown.classicchars import DistributedVampireMickey/AI
from toontown.classicchars import DistributedMinnie/AI
from toontown.classicchars import DistributedWitchMinnie/AI
from toontown.classicchars import DistributedGoofy/AI
from toontown.classicchars import DistributedSuperGoofy/AI
from toontown.classicchars import DistributedDaisy/AI
from toontown.classicchars import DistributedSockHopDaisy/AI
from toontown.classicchars import DistributedChip/AI
from toontown.classicchars import DistributedPoliceChip/AI
from toontown.classicchars import DistributedDale/AI
from toontown.classicchars import DistributedJailbirdDale/AI
from toontown.classicchars import DistributedGoofySpeedway/AI
from toontown.classicchars import DistributedDonald/AI
from toontown.classicchars import DistributedFrankenDonald/AI
from toontown.classicchars import DistributedDonaldDock/AI
from toontown.classicchars import DistributedPluto/AI
from toontown.classicchars import DistributedWesternPluto/AI
from toontown.safezone import DistributedTrolley/AI
from toontown.safezone import DistributedPartyGate/AI
from toontown.suit import DistributedSuitPlanner/AI
from toontown.suit import DistributedSuitBase/AI
from toontown.suit import DistributedSuit/AI
from toontown.suit import DistributedTutorialSuit/AI
from toontown.suit import DistributedFactorySuit/AI
from toontown.suit import DistributedMintSuit/AI
from toontown.suit import DistributedBoardOfficeSuit/AI
from toontown.suit import DistributedStageSuit/AI
from toontown.suit import DistributedSellbotBoss/AI
from toontown.suit import DistributedCashbotBoss/AI
from toontown.coghq import DistributedCashbotBossSafe/AI
from toontown.coghq import DistributedCashbotBossCrane/AI
from toontown.suit import DistributedCashbotBossGoon/AI
from toontown.suit import DistributedBoardbotBoss/AI
from toontown.battle import DistributedBattleBase/AI
from toontown.battle import DistributedBattle/AI
from toontown.battle import DistributedBattleBldg/AI
from toontown.tutorial import DistributedBattleTutorial/AI
from toontown.coghq import DistributedBattleFactory/AI
from toontown.battle import DistributedBattleFinal/AI
from toontown.safezone import DistributedBoat/AI
from toontown.safezone import DistributedButterfly/AI
from toontown.safezone import DistributedMMPiano/AI
from toontown.safezone import DistributedDGFlower/AI
from toontown.fishing import DistributedFishingPond/AI
from toontown.fishing import DistributedFishingTarget/AI
from toontown.fishing import DistributedPondBingoManager/AI
from toontown.safezone import DistributedFishingSpot/AI
from toontown.estate import DistributedCannon/AI
from toontown.estate import DistributedTarget/AI
from toontown.minigame import DistributedMinigame/AI
from toontown.minigame import DistributedMinigameTemplate/AI
from toontown.minigame import DistributedRaceGame/AI
from toontown.minigame import DistributedCannonGame/AI
from toontown.minigame import DistributedPhotoGame/AI
from toontown.minigame import DistributedPatternGame/AI
from toontown.minigame import DistributedRingGame/AI
from toontown.minigame import DistributedTagGame/AI
from toontown.minigame import DistributedMazeGame/AI
from toontown.minigame import DistributedTugOfWarGame/AI
from toontown.minigame import DistributedCatchGame/AI
from toontown.minigame import DistributedDivingGame/AI
from toontown.minigame import DistributedTargetGame/AI
from toontown.estate import EstateManager/AI
from toontown.estate import DistributedEstate/AI
from toontown.estate import DistributedHouse/AI
from toontown.estate import DistributedHouseInterior/AI
from toontown.estate import DistributedGarden/AI
from toontown.shtiker import DeleteManager/AI
from toontown.ai import NewsManager/AI
from toontown.shtiker import PurchaseManager/AI
from toontown.shtiker import NewbiePurchaseManager/AI
from toontown.safezone import SafeZoneManager/AI
from toontown.tutorial import TutorialManager/AI
from toontown.catalog import CatalogManager/AI
from toontown.safezone import DistributedTreasure/AI
from toontown.safezone import DistributedSZTreasure/AI
from toontown.safezone import DistributedEFlyingTreasure/AI
from toontown.coghq import DistributedCashbotBossTreasure/AI
from toontown.building import DistributedTrophyMgr/AI
from toontown.building import DistributedBuilding/AI
from toontown.building import DistributedAnimBuilding/AI
from toontown.building import DistributedToonInterior/AI
from toontown.building import DistributedToonHallInterior/AI
from toontown.building import DistributedSuitInterior/AI
from toontown.building import DistributedHQInterior/AI
from toontown.building import DistributedGagshopInterior/AI
from toontown.building import DistributedPetshopInterior/AI
from toontown.building import DistributedKartShopInterior/AI
from toontown.building import DistributedDoor/AI
from toontown.building import DistributedAnimDoor/AI
from toontown.building import DistributedLightSwitch/AI
from toontown.estate import DistributedHouseDoor/AI
from toontown.coghq import DistributedCogHQDoor/AI
from toontown.coghq import DistributedSellbotHQDoor/AI
from toontown.toon import DistributedNPCToonBase/AI
from toontown.toon import DistributedNPCToon/AI
from toontown.toon import DistributedNPCHQOfficer/AI
from toontown.toon import DistributedNPCSpecialQuestGiver/AI
from toontown.toon import DistributedNPCFlippyInToonHall/AI
from toontown.toon import DistributedNPCScientist/AI
from toontown.toon import DistributedNPCClerk/AI
from toontown.toon import DistributedNPCTailor/AI
from toontown.toon import DistributedNPCBlocker/AI
from toontown.toon import DistributedNPCFisherman/AI
from toontown.toon import DistributedNPCPartyPerson/AI
from toontown.toon import DistributedNPCPetclerk/AI
from toontown.toon import DistributedNPCKartClerk/AI
from toontown.toon import DistributedNPCLoopyG/AI
from toontown.toon import DistributedNPCInvisible/AI
from toontown.building import DistributedKnockKnockDoor/AI
from toontown.building import DistributedElevator/AI
from toontown.building import DistributedElevatorFSM/AI
from toontown.building import DistributedElevatorExt/AI
from toontown.building import DistributedElevatorInt/AI
from toontown.coghq import DistributedFactoryElevatorExt/AI
from toontown.coghq import DistributedMintElevatorExt/AI
from toontown.coghq.boardbothq import DistributedBoardOfficeElevatorExt/AI
from toontown.coghq import DistributedLawOfficeElevatorExt/AI
from toontown.coghq import DistributedLawOfficeElevatorInt/AI
from toontown.building import DistributedElevatorFloor/AI
from toontown.building import DistributedBossElevator/AI
from toontown.building import DistributedVPElevator/AI
from toontown.building import DistributedCFOElevator/AI
from toontown.building import DistributedCJElevator/AI
from toontown.building import DistributedBBElevator/AI
from toontown.building import DistributedCMElevator/AI
from toontown.building import DistributedBoardingParty/AI
from toontown.building import DistributedTutorialInterior/AI
from toontown.estate import DistributedBankMgr/AI
from toontown.estate import DistributedMailbox/AI
from toontown.estate import DistributedFurnitureManager/AI
from toontown.estate import DistributedFurnitureItem/AI
from toontown.estate import DistributedBank/AI
from toontown.estate import DistributedCloset/AI
from toontown.estate import DistributedTrunk/AI
from toontown.estate import DistributedPhone/AI
from toontown.effects import DistributedFireworkShow/AI
from toontown.estate import DistributedFireworksCannon/AI
from toontown.coghq import LobbyManager/AI
from otp.level import DistributedLevel/AI
from otp.level import DistributedEntity/AI
from otp.level import DistributedInteractiveEntity/AI
from toontown.coghq import DistributedFactory/AI
from toontown.coghq import DistributedLawOffice/AI
from toontown.coghq import DistributedLawOfficeFloor/AI
from toontown.coghq import DistributedLift/AI
from toontown.coghq import DistributedDoorEntity/AI
from toontown.coghq import DistributedSwitch/AI
from toontown.coghq import DistributedButton/AI
from toontown.coghq import DistributedTrigger/AI
from toontown.coghq import DistributedCrushableEntity/AI
from toontown.coghq import DistributedCrusherEntity/AI
from toontown.coghq import DistributedStomper/AI
from toontown.coghq import DistributedStomperPair/AI
from toontown.coghq import DistributedLaserField/AI
from toontown.coghq import DistributedGolfGreenGame/AI
from toontown.coghq import DistributedSecurityCamera/AI
from toontown.coghq import DistributedMover/AI
from toontown.coghq import DistributedElevatorMarker/AI
from toontown.coghq import DistributedBarrelBase/AI
from toontown.coghq import DistributedGagBarrel/AI
from toontown.coghq import DistributedBeanBarrel/AI
from toontown.coghq import DistributedHealBarrel/AI
from toontown.coghq import DistributedGrid/AI
from toontown.coghq import ActiveCell/AI
from toontown.coghq import DirectionalCell/AI
from toontown.coghq import CrusherCell/AI
from toontown.coghq import DistributedCrate/AI
from toontown.coghq import DistributedSinkingPlatform/AI
from toontown.suit import DistributedGoon/AI
from toontown.suit import DistributedGridGoon/AI
from toontown.coghq import BattleBlocker/AI
from toontown.ai import DistributedAprilToonsMgr/AI
from toontown.ai import DistributedBlackCatMgr/AI
from toontown.ai import DistributedPolarBearMgr/AI
from toontown.ai import DistributedPolarPlaceEffectMgr/AI
from toontown.ai import DistributedSofieListenerMgr/AI
from toontown.ai import DistributedGreenToonEffectMgr/AI
from toontown.ai import DistributedResistanceEmoteMgr/AI
from toontown.ai import DistributedScavengerHuntTarget/AI
from toontown.ai import DistributedTrickOrTreatTarget/AI
from toontown.ai import DistributedWinterCarolingTarget/AI
from toontown.coghq import DistributedMint/AI
from toontown.coghq import DistributedMintRoom/AI
from toontown.coghq import DistributedMintBattle/AI
from toontown.coghq.boardbothq import DistributedBoardOffice/AI
from toontown.coghq.boardbothq import DistributedBoardOfficeRoom/AI
from toontown.coghq.boardbothq import DistributedBoardOfficeBattle/AI
from toontown.coghq import DistributedStage/AI
from toontown.coghq import DistributedStageRoom/AI
from toontown.coghq import DistributedStageBattle/AI
from toontown.pets.PetDCImports/AI import *
from toontown.pets import DistributedPetProxy/AI
from toontown.pets import DistributedPublicPet/AI
from toontown.pets import DistributedPublicPetMgr/AI
from toontown.coghq.InGameEditorDCImports/AI import *
from toontown.distributed import ToontownDistrict/AI
from toontown.distributed import ToontownDistrictStats/AI
from toontown.racing import DistributedVehicle/AI
from toontown.racing import DistributedStartingBlock/AI
from toontown.racing import DistributedRace/AI
from toontown.racing import DistributedKartPad/AI
from toontown.racing import DistributedRacePad/AI
from toontown.racing import DistributedViewPad/AI
from toontown.racing import DistributedStartingBlock/AI
from toontown.racing import DistributedLeaderBoard/AI
from toontown.racing import DistributedGag/AI
from toontown.racing import DistributedProjectile/AI
from toontown.racing.DistributedStartingBlock/AI import DistributedViewingBlock/AI
from toontown.uberdog.ClientServicesManager/UD import ClientServicesManager/UD
from toontown.uberdog.DistributedDeliveryManager/AI/UD import DistributedDeliveryManager/AI/UD
from toontown.uberdog.DistributedDataStoreManager/AI/UD import DistributedDataStoreManager/AI/UD
from toontown.suit import DistributedLawbotBoss/AI
from toontown.coghq import DistributedLawbotBossGavel/AI
from toontown.suit import DistributedLawbotBossSuit/AI
from toontown.coghq import DistributedLawbotCannon/AI
from toontown.coghq import DistributedLawbotChair/AI
from toontown.estate import DistributedLawnDecor/AI
from toontown.estate import DistributedGardenPlot/AI
from toontown.estate import DistributedGardenBox/AI
from toontown.estate import DistributedFlower/AI
from toontown.estate import DistributedGagTree/AI
from toontown.estate import DistributedStatuary/AI
from toontown.estate import DistributedToonStatuary/AI
from toontown.estate import DistributedChangingStatuary/AI
from toontown.estate import DistributedAnimatedStatuary/AI
from toontown.estate import DistributedPlantBase/AI
from toontown.estate import DistributedLawnDecor/AI
from toontown.events import CharityScreen/AI
from toontown.minigame import DistributedTravelGame/AI
from toontown.minigame import DistributedPairingGame/AI
from toontown.minigame import DistributedVineGame/AI
from toontown.golf import DistributedPhysicsWorld/AI
from toontown.golf import DistributedGolfHole/AI
from toontown.golf import DistributedGolfCourse/AI
from toontown.parties import DistributedParty/AI
from toontown.parties import DistributedPartyActivity/AI
from toontown.parties import DistributedPartyTeamActivity/AI
from toontown.parties import DistributedPartyCannon/AI
from toontown.parties import DistributedPartyCannonActivity/AI
from toontown.parties import DistributedPartyCatchActivity/AI
from toontown.parties import DistributedPartyWinterCatchActivity/AI
from toontown.parties import DistributedPartyCogActivity/AI
from toontown.parties import DistributedPartyWinterCogActivity/AI
from toontown.parties import DistributedPartyFireworksActivity/AI
from toontown.parties import DistributedPartyDanceActivityBase/AI
from toontown.parties import DistributedPartyDanceActivity/AI
from toontown.parties import DistributedPartyDance20Activity/AI
from toontown.parties import DistributedPartyValentineDanceActivity/AI
from toontown.parties import DistributedPartyValentineDance20Activity/AI
from toontown.parties import DistributedPartyTrampolineActivity/AI
from toontown.parties import DistributedPartyValentineTrampolineActivity/AI
from toontown.parties import DistributedPartyVictoryTrampolineActivity/AI
from toontown.parties import DistributedPartyWinterTrampolineActivity/AI
from toontown.parties import DistributedPartyTugOfWarActivity/AI
from toontown.parties import DistributedPartyJukeboxActivityBase/AI
from toontown.parties import DistributedPartyJukeboxActivity/AI
from toontown.parties import DistributedPartyJukebox40Activity/AI
from toontown.parties import DistributedPartyValentineJukeboxActivity/AI
from toontown.parties import DistributedPartyValentineJukebox40Activity/AI
from toontown.friends import TTPlayerFriendsManager/UD
from toontown.friends import TTAFriendsManager/UD
from toontown.uberdog import TTSpeedchatRelay/UD
from toontown.safezone import DistributedGolfKart/AI
from toontown.safezone import DistributedPicnicBasket/AI
from toontown.safezone import DistributedGameTable/AI
from toontown.distributed import DistributedTimer/AI
from toontown.suit import DistributedBossbotBoss/AI
from toontown.coghq import DistributedCogKart/AI
from toontown.coghq import DistributedCountryClub/AI
from toontown.coghq import DistributedCountryClubRoom/AI
from toontown.coghq import DistributedMoleField/AI
from toontown.coghq import DistributedCountryClubBattle/AI
from toontown.building import DistributedClubElevator/AI
from toontown.coghq import DistributedMaze/AI
from toontown.battle import DistributedBattleWaiters/AI
from toontown.coghq import DistributedFoodBelt/AI
from toontown.coghq import DistributedBanquetTable/AI
from toontown.battle import DistributedBattleDiners/AI
from toontown.coghq import DistributedGolfSpot/AI
from toontown.minigame import DistributedIceGame/AI
from toontown.minigame import DistributedCogThiefGame/AI
from toontown.minigame import DistributedTwoDGame/AI
from toontown.safezone import DistributedChineseCheckers/AI
from toontown.safezone import DistributedCheckers/AI
from toontown.safezone import DistributedFindFour/AI
from toontown.uberdog.DistributedMailManager/AI/UD import DistributedMailManager/AI/UD
from toontown.rpc.AwardManager/UD import AwardManager/UD
from toontown.uberdog.DistributedCpuInfoMgr/AI/UD import DistributedCpuInfoMgr/AI/UD
from toontown.uberdog.DistributedSecurityMgr/AI/UD import DistributedSecurityMgr/AI/UD
from toontown.uberdog.DistributedInGameNewsMgr/AI/UD import DistributedInGameNewsMgr/AI/UD
from toontown.uberdog.DistributedWhitelistMgr/AI/UD import DistributedWhitelistMgr/AI/UD
from toontown.coderedemption.TTCodeRedemptionMgr/AI/UD import TTCodeRedemptionMgr/AI/UD
from toontown.distributed.NonRepeatableRandomSourceAI import NonRepeatableRandomSourceAI
from toontown.distributed.NonRepeatableRandomSourceUD import NonRepeatableRandomSourceUD
from toontown.ai.DistributedPhaseEventMgr/AI import DistributedPhaseEventMgr/AI
from toontown.ai.DistributedHydrantZeroMgr/AI import DistributedHydrantZeroMgr/AI
from toontown.ai.DistributedMailboxZeroMgr/AI import DistributedMailboxZeroMgr/AI
from toontown.ai.DistributedTrashcanZeroMgr/AI import DistributedTrashcanZeroMgr/AI
from toontown.ai import DistributedSillyMeterMgr/AI
from toontown.cogdominium import DistributedCogdoInterior/AI
from toontown.cogdominium import DistributedCogdoBattleBldg/AI
from toontown.cogdominium import DistributedCogdoElevatorExt/AI
from toontown.cogdominium import DistributedCogdoElevatorInt/AI
from toontown.cogdominium import DistributedCogdoBarrel/AI
from toontown.cogdominium import DistCogdoGame/AI
from toontown.cogdominium import DistCogdoLevelGame/AI
from toontown.cogdominium import DistCogdoBoardroomGame/AI
from toontown.cogdominium import DistCogdoCraneGame/AI
from toontown.cogdominium import DistCogdoMazeGame/AI
from toontown.cogdominium import DistCogdoFlyingGame/AI
from toontown.cogdominium import DistCogdoCrane/AI
from toontown.cogdominium import DistCogdoCraneMoneyBag/AI
from toontown.cogdominium import DistCogdoCraneCog/AI
from toontown.betaevent import DistributedEvent/AI
from toontown.betaevent import DistributedBetaEvent/AI
from toontown.betaevent import DistributedBetaEventTTC/AI
from toontown.weather import DistributedWeatherCycle/AI
from toontown.weather import DistributedWeatherStorm/AI
from toontown.club import DistributedToonClub/AI
from toontown.environment import DistributedDayTimeManager/AI
from toontown.environment import DistributedRainManager/AI
from toontown.environment import DistributedWeatherMGR/AI


struct GiftItem {
  blob Item;
  string giftTag;
};

struct gardenSpecial {
  uint8 index;
  uint8 count;
};

struct simpleMail {
  uint64 msgId;
  uint32 senderId;
  uint16 year;
  uint8 month;
  uint8 day;
  string body;
};

struct invite {
  uint64 inviteKey;
  uint64 partyId;
  uint8 status;
};

struct decoration {
  uint8 decorId;
  uint8 x;
  uint8 y;
  uint8 h;
};

struct activity {
  uint8 activityId;
  uint8 x;
  uint8 y;
  uint8 h;
};

struct party {
  uint64 partyId;
  uint32 hostId;
  uint16 startYear;
  uint8 startMonth;
  uint8 startDay;
  uint8 startHour;
  uint8 startMinute;
  uint16 endYear;
  uint8 endMonth;
  uint8 endDay;
  uint8 endHour;
  uint8 endMinute;
  uint8 isPrivate;
  uint8 inviteTheme;
  activity activities[];
  decoration decors[];
  uint8 status;
};

struct partyReply {
  uint32 inviteeId;
  uint8 status;
};

struct repliesForOneParty {
  uint64 partyId;
  partyReply partyReplies[];
};

struct publicPartyInfo {
  uint32 shardId;
  uint32 zoneId;
  uint8 numberOfGuests;
  string hostName;
  uint8[] activityIds;
  uint16 minLeft;
};

struct jukeboxSongInfo {
  uint8/10 phase;
  string fileName;
};

struct partyCloudColor {
  uint16 cloudNumber;
  uint8/100 r;
  uint8/100 g;
  uint8/100 b;
};

struct datetime {
  uint16 year;
  uint8 month;
  uint8 day;
  uint8 hour;
  uint8 minutes;
  uint8 seconds;
};

dclass ToontownDistrict : DistributedDistrict {
  setParentingRules(string, string) broadcast ram;
  allowAHNNLog(bool) broadcast required ram;
};

dclass ToontownDistrictStats : DistributedObject {
  settoontownDistrictId(uint32) broadcast required ram;
  setAvatarCount(uint32) broadcast required ram;
  setNewAvatarCount(uint32) broadcast required ram;
  setInvasionStatus(uint8) broadcast required ram;
  setStats : setAvatarCount, setNewAvatarCount;
};

dclass WelcomeValleyManager : DistributedObject {
  clientSetZone(uint32) airecv clsend;
  requestZoneIdMessage(uint32, uint16) airecv clsend;
  requestZoneIdResponse(uint32, uint16);
};

dclass DistributedAnimatedProp : DistributedObject {
  setPropId(uint16) required broadcast ram;
  setAvatarInteract(uint32) required broadcast ram;
  requestInteract() airecv clsend;
  rejectInteract();
  requestExit() airecv clsend;
  avatarExit(uint32) broadcast;
  setState(string, int16) required broadcast ram;
};

typedef int16 pair16[2];

dclass DistributedToon : DistributedPlayer {
  setDNAString(blob) required broadcast ownrecv db;
  setGM(uint16 = 0) required broadcast ownrecv db;
  setMoney(uint16 = 0) required ownrecv db;
  setMaxBankMoney(uint32 maxMoney = 15000) required broadcast ownrecv db;
  setMaxMoney(uint16 maxMoney = 500) required broadcast ownrecv db;
  setBankMoney(uint64 money = 0) required ownrecv db;
  setMaxHp(int16 = 15) required broadcast ownrecv db;
  setHp(int16 = 15) required broadcast ownrecv db;
  setUber(int16) required broadcast ownrecv db;
  toonUp(uint16) broadcast ownrecv;
  takeDamage(uint16) broadcast ownrecv;
  setBattleId(uint32 = 0) required broadcast ram;
  setToonExp(uint32 exp = 0) required broadcast ownrecv db;
  setToonLevel(uint8 level = 0) required broadcast ram db;
  setTrueFriends(uint32[] = []) ownrecv required db airecv;
  setTrueFriendRequest(uint32[] = [0, 0]) ram airecv;
  setExperience(blob = [0*16]) required broadcast db;
  setMaxCarry(uint8 = 20) required ownrecv db;
  setTrackAccess(uint16[] = [0,0,0,0,1,1,0,0]) required broadcast ownrecv db;
  setTrackProgress(int8 = -1, uint32 = 0) required ownrecv db;
  setTrackBonusLevel(int8[] = [-1,-1,-1,-1,-1,-1,-1,-1,-1]) required broadcast ownrecv db;
  setInventory(blob = [0*7, 0*7, 0*7, 0*7, 1, 0*6, 1, 0*6, 0*7, 0*7]) required ownrecv db;
  setMaxNPCFriends(uint16 = 16) required ownrecv db;
  setNPCFriendsDict(FriendEntry[] = []) required ownrecv db;
  setDefaultShard(uint32 = 0) required ownrecv broadcast db;
  setDefaultZone(uint32 = 0) required ownrecv broadcast db;
  setShtickerBook(blob = []) required ownrecv db;
  setZonesVisited(uint32[] = [ 2000 ]) required ownrecv db;
  setHoodsVisited(uint32[] = [ 2000 ]) required ownrecv db;
  setInterface(blob = []) required ownrecv db;
  setLastHood(uint32 = 0) required ownrecv broadcast db;
  setTutorialAck(uint8) required ownrecv db;
  setMaxClothes(uint32 = 10) required ownrecv db;
  setClothesTopsList(uint8[] = []) required ownrecv db;
  setClothesBottomsList(uint8[] = []) required ownrecv db;
  setMaxAccessories(uint32 = 0) required ownrecv db;
  setHatList(uint8[] = []) required ownrecv db;
  setGlassesList(uint8[] = []) required ownrecv db;
  setBackpackList(uint8[] = []) required ownrecv db;
  setShoesList(uint8[] = []) required ownrecv db;
  setHat(uint8 = 0, uint8 = 0, uint8 = 0) required broadcast db ownrecv;
  setGlasses(uint8 = 0, uint8 = 0, uint8 = 0) required broadcast db ownrecv;
  setBackpack(uint8 = 0, uint8 = 0, uint8 = 0) required broadcast db ownrecv;
  setShoes(uint8 = 0, uint8 = 0, uint8 = 0) required broadcast db ownrecv;
  setGardenSpecials(gardenSpecial [] = []) required ownrecv db airecv;
  setEarnedExperience(uint16[]) ownrecv;
  setTunnelIn(int16, int16/10, int16/10, int16/10, int16/100, int32/100) ownsend broadcast;
  setTunnelOut(int16, int16/10, int16/10, int16/10, int16/10, int16/100, int32/100) ownsend broadcast;
  setAnimState(char [0-1024], int16/1000, int16) broadcast ram ownsend airecv;
  setEmoteState(int16, int16/1000, int16) broadcast ram ownsend;
  setEmoteAccess(uint8[] = [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) required ownrecv db;
  setCustomMessages(uint16[] = []) required ownrecv db;
  setSleepAutoReply(uint32) broadcast clsend ownrecv;
  setResistanceMessages(pair16 [] = []) required ownrecv db;
  setPetTrickPhrases(uint8[] = [0]) required ownrecv db;
  setCatalogSchedule(uint16 = 0, uint32 = 0) required ownrecv db;
  setCatalog(blob = [], blob = [], blob = []) required ownrecv db;
  setMailboxContents(blob = []) required ownrecv db;
  setDeliverySchedule(blob = []) required ownrecv db airecv;
  setGiftSchedule(blob = []) required ownrecv db airecv;
  setAwardMailboxContents(blob = []) required ownrecv db;
  setAwardSchedule(blob = []) required ownrecv db airecv;
  setAwardNotify(uint8 = 0) required ownrecv db;
  setCatalogNotify(uint8 = 0, uint8 = 0) required ownrecv db;
  playSplashEffect(int16/10, int16/10, int16/10) broadcast ownsend;
  setWhisperSCToontaskFrom(uint32, uint32, uint32, uint32, uint8) ownrecv clsend;
  setSCToontask(uint32, uint32, uint32, uint8) broadcast ownsend;
  reqSCResistance(uint16, uint32 []) ownsend airecv;
  setSCResistance(uint16, uint32 []) broadcast ownrecv;
  setSpeedChatStyleIndex(uint8 = 1) required ownsend broadcast db;
  setTrophyScore(uint16) broadcast ownrecv ram;
  setTeleportAccess(uint32[] = []) required ownrecv db;
  setScavengerHunt(uint32[] = []) required ownrecv db;
  checkTeleportAccess(uint16) airecv ownsend;
  checkTeleportAccessResponse(uint16) ownrecv;
  battleSOS(uint32) ownrecv clsend;
  teleportQuery(uint32) ownrecv clsend;
  teleportResponse(uint32, int8, uint32, uint32, uint32) ownrecv clsend;
  teleportResponseToAI(uint32, int8, uint32, uint32, uint32, uint32) ownsend airecv;
  teleportGiveup(uint32) ownrecv clsend;
  teleportGreeting(uint32) broadcast ownsend;
  setCogStatus(uint32[] = [1 * 40]) required ownrecv db;
  setCogCount(uint32[] = [0 * 40]) required ownrecv db;
  setCogRadar(uint8[] = [0 * 5]) required ownrecv db;
  setBuildingRadar(uint8[] = [0 * 5]) required ownrecv db;
  setCogLevels(uint8[] = [0 * 5]) required broadcast ownrecv db;
  setCogReviveLevels(int8[] = [-1 * 5]) required broadcast ownrecv db;
  setCogTypes(uint8[] = [0 * 5]) required broadcast ownrecv db;
  setCogParts(uint32[] = [0 * 5]) required broadcast ownrecv db;
  setCogMerits(uint16[] = [0 * 5]) required ownrecv db;
  setPromotionStatus(uint8[] = [0 * 5]) required broadcast ownrecv db;
  setCogIndex(int8) broadcast ram;
  setDisguisePageFlag(int8) ownrecv;
  setSosPageFlag(int8) ownrecv;
  setHouseId(uint32 = 0) required ownrecv db;
  setQuests(uint32[] = []) required broadcast ownrecv db;
  setQuestHistory(uint16[] = []) required broadcast ownrecv db;
  setQuestCarryLimit(uint8 = 4) required ownrecv db;
  requestDeleteQuest(uint32[]) ownsend airecv;
  setCheesyEffect(int16 = 0, uint32 = 0, uint32 = 0) required broadcast ownrecv db;
  setCheesyEffects(int16[] = [0]) required broadcast ownrecv db;
  setGhostMode(uint8) broadcast ownrecv ram;
  setPosIndex(uint8 = 0) required ownrecv db;
  setFishCollection(uint8[] = [], uint8[] = [], uint16[] = []) required ownrecv db;
  setMaxFishTank(uint8 = 20) required ownrecv db;
  setFishTank(uint8[] = [], uint8[] = [], uint16[] = []) required ownrecv db;
  setFishingRod(uint8 = 0) required broadcast ownrecv db;
  setFishingRods(uint8[] = [0]) required broadcast ownrecv db;
  setFishingTrophies(uint8[] = []) required ownrecv db;
  setFlowerCollection(uint8[] = [], uint8[] = []) required ownrecv db;
  setFlowerBasket(uint8[] = [], uint8[] = []) required ownrecv db;
  setMaxFlowerBasket(uint8 = 20) required ownrecv db;
  setGardenTrophies(uint8[] = []) required ownrecv db;
  setShovel(uint8 = 0) required broadcast ownrecv db;
  setShovelSkill(uint32 = 0) required ownrecv db;
  setWateringCan(uint8 = 0) required broadcast ownrecv db;
  setWateringCanSkill(uint32 = 0) required ownrecv db;
  promoteShovel(uint8) ownrecv;
  promoteWateringCan(uint8) ownrecv;
  reactivateWater() ownrecv;
  presentPie(int16/10 x, int16/10 y, int16/10 z, int16/10 h, int32 timestamp) broadcast ownsend;
  tossPie(int16/10 x, int16/10 y, int16/10 z, int16/10 h, uint8 sequence, uint8 power, uint8 throwType, int32 timestamp) broadcast ownsend;
  pieSplat(int16/10, int16/10, int16/10, uint8, uint8, int32) broadcast ownsend;
  setPieType(uint8) broadcast ownrecv ram;
  setNumPies(uint16) broadcast ownrecv ram;
  catalogGenClothes(uint32) broadcast ownrecv;
  catalogGenAccessories(uint32) broadcast ownrecv;
  setPetId(uint32 = 0) required broadcast ownrecv db;
  setPetMovie(uint32, uint8) ownsend airecv;
  setPetTutorialDone(uint8 = 0) required ownsend airecv db;
  setFishBingoTutorialDone(uint8 = 0) required ownsend airecv db;
  setFishBingoMarkTutorialDone(uint8 = 0) required ownsend airecv db;
  setKartBodyType(int8 = -1) required broadcast ownrecv db;
  setKartBodyColor(int8 = -1) required broadcast ownrecv db;
  setKartAccessoryColor(int8 = -1) required broadcast ownrecv db;
  setKartEngineBlockType(int8 = -1) required broadcast ownrecv db;
  setKartSpoilerType(int8 = -1) required broadcast ownrecv db;
  setKartFrontWheelWellType(int8 = -1) required broadcast ownrecv db;
  setKartBackWheelWellType(int8 = -1) required broadcast ownrecv db;
  setKartRimType(int8 = -1) required broadcast ownrecv db;
  setKartDecalType(int8 = -1) required broadcast ownrecv db;
  updateKartDNAField(int8, int8) ownsend airecv;
  addOwnedAccessory(int8) ownsend airecv;
  removeOwnedAccessory(int8) ownsend airecv;
  setTickets(uint32 = 200) required broadcast ownrecv db;
  setKartingHistory(uint8 [16] = [0*16]) required ownrecv db;
  setKartingTrophies(uint8 [33] = [0*33]) required ownrecv db;
  setKartingPersonalBest(uint32/1000 [6] = [0*6]) required ownrecv db;
  setKartingPersonalBest2(uint32/1000 [12] = [0*12]) required ownrecv db;
  setKartAccessoriesOwned(int8 [16] = [-1*16]) required broadcast ownrecv db;
  setCurrentKart(uint32) broadcast ownrecv ram;
  squish(uint8) ownsend airecv;
  announceBingo() broadcast ownrecv;
  trickOrTreatTargetMet(uint32) ownrecv;
  trickOrTreatMilestoneMet() ownrecv;
  winterCarolingTargetMet(uint32) ownrecv;
  setCogSummonsEarned(uint8[] = [0*40]) required ownrecv db;
  reqCogSummons(char [0-256], uint32) ownsend airecv;
  cogSummonsResponse(string, uint32, uint32) ownrecv;
  reqUseSpecial(int32) ownsend airecv;
  useSpecialResponse(string) ownrecv;
  setGardenStarted(uint8 = 0) required ownrecv db;
  sendToGolfCourse(uint32) ownrecv;
  setGolfHistory(uint16 [18] = [0*18]) required ownrecv db;
  setPackedGolfHoleBest(uint8 [18] = [0*18]) required ownrecv db;
  setGolfCourseBest(uint8 [3] = [0*3]) required ownrecv db;
  setUnlimitedSwing(uint8) broadcast ownrecv ram;
  logSuspiciousEvent(char [0-1024]) ownsend airecv;
  logMessage(char [0-1024]) ownsend airecv;
  forceLogoutWithNotify() ownrecv;
  setPinkSlips(uint8 = 0) required ownrecv db;
  setNametagStyle(uint8 = 1) required broadcast ownrecv db;
  setNametagStyles(uint8[] = [0]) required broadcast ownrecv db;
  setMail(simpleMail []) ownrecv airecv ram;
  setNumMailItems(uint32) airecv;
  setSimpleMailNotify(uint8) ownrecv airecv;
  setInvites(invite []) ownrecv airecv ram;
  setPartiesInvitedTo(party []) ownrecv airecv ram;
  setHostedParties(party []) ownrecv airecv ram;
  setPartyReplies(repliesForOneParty []) ownrecv airecv ram;
  updateInvite(uint64, uint8) ownrecv airecv;
  updateReply(uint64, uint64, uint8) ownrecv airecv;
  setPartyCanStart(uint64) ownrecv airecv;
  setPartyStatus(uint64, uint8) ownrecv airecv;
  announcePartyStarted(uint64) ownrecv;
  setAchievements(uint16[] = []) required broadcast ownrecv db;
  setNeverStartedPartyRefunded(uint64, int8, uint16) ownrecv;
  refundParty(uint16) ownrecv airecv ram;
  setModuleInfo(string []) airecv clsend;
  setDISLname(string) ram;
  setDISLid(uint32) ram db airecv;
  flagAv(uint32, uint16, string []) airecv ownsend;
  setAnimalSound(uint8 index) ram broadcast ownrecv;
  setBuffs(uint32[] = []) required ownrecv db;
  magicTeleportRequest(uint32 requesterId) ownrecv;
  magicTeleportResponse(uint32 requesterId, uint32 hoodId) ownsend airecv;
  magicTeleportInitiate(uint32 hoodId, uint32 zoneId) ownrecv;
  notifyExpReward(int32 level, uint8 type) broadcast ownrecv;
  requestNametagStyle(uint8) airecv ownsend;
  requestFishingRod(uint8) airecv ownsend;
  requestCheesyEffects(uint8) airecv ownsend;
  setWarningCount(uint8) ownrecv db;
  setStats(uint32[] = [0*28]) required ownrecv db;
  setInteriorLayout(uint8 = 0) required ownrecv db;
  setRedeemedCodes(string [] = []) required ownrecv db;
  setTrainingPoints(uint8 = 0) required ownrecv db;
  setSpentTrainingPoints(uint8[] = [0, 0, 0, 0, 2, 2, 0, 0]) required ownrecv db;
  requestSkillSpend(uint8) ownsend airecv;
  requestSkillReturn(uint8) ownsend airecv;
  setCerts(string[] = []) required broadcast ownrecv db;
};

dclass DistributedCCharBase : DistributedObject {
  setChat(uint32, uint32, uint32) broadcast;
  fadeAway() broadcast;
  setWalk(string, string, int16) required broadcast ram;
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  setNearbyAvatarChat(char [0-1024]) airecv clsend;
  setNearbyAvatarSC(uint16) airecv clsend;
  setNearbyAvatarSCCustom(uint16) airecv clsend;
  setNearbyAvatarSCToontask(uint32, uint32, uint32, uint8) airecv clsend;
};

dclass DistributedMickey : DistributedCCharBase {
};

dclass DistributedVampireMickey : DistributedMickey {
};

dclass DistributedWitchMinnie : DistributedMickey {
};

dclass DistributedMinnie : DistributedCCharBase {
};

dclass DistributedGoofy : DistributedCCharBase {
};

dclass DistributedDaisy : DistributedCCharBase {
};

dclass DistributedSockHopDaisy : DistributedDaisy {
};

dclass DistributedChip : DistributedCCharBase {
};

dclass DistributedPoliceChip : DistributedChip {
};

dclass DistributedDale : DistributedCCharBase {
  setFollowChip(string, string, int16, int16/100, int16/100) broadcast ram;
  setChipId(uint32) required broadcast ram;
};

dclass DistributedJailbirdDale : DistributedDale {
};

dclass DistributedDonald : DistributedCCharBase {
};

dclass DistributedFrankenDonald : DistributedDonald {
};

dclass DistributedDonaldDock : DistributedCCharBase {
};

dclass DistributedPluto : DistributedCCharBase {
};

dclass DistributedWesternPluto : DistributedPluto {
};

dclass DistributedGoofySpeedway : DistributedCCharBase {
};

dclass DistributedSuperGoofy : DistributedGoofySpeedway {
};

dclass DistributedPartyGate : DistributedObject {
  getPartyList(uint32) airecv clsend;
  partyChoiceRequest(uint32, uint64, uint64) airecv clsend;
  listAllPublicParties(publicPartyInfo []);
  partyRequestDenied(uint8);
  setParty(publicPartyInfo, uint32 hostId);
};

dclass DistributedTrolley : DistributedObject {
  setState(string, int16) broadcast ram;
  fillSlot0(uint32) broadcast ram;
  fillSlot1(uint32) broadcast ram;
  fillSlot2(uint32) broadcast ram;
  fillSlot3(uint32) broadcast ram;
  emptySlot0(uint32, int16) broadcast ram;
  emptySlot1(uint32, int16) broadcast ram;
  emptySlot2(uint32, int16) broadcast ram;
  emptySlot3(uint32, int16) broadcast ram;
  requestBoard() airecv clsend;
  rejectBoard(uint32);
  requestExit() airecv clsend;
  setMinigameZone(uint32, uint16);
};

dclass DistributedSuitPlanner : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  suitListQuery() airecv clsend;
  suitListResponse(uint8[]);
  buildingListQuery() airecv clsend;
  buildingListResponse(uint8[]);
};

dclass DistributedSuitBase : DistributedObject {
  denyBattle();
  setDNAString(blob) required broadcast ram;
  setLevelDist(int16) required broadcast ram;
  setBrushOff(int16) broadcast;
  setWaiter(uint8) broadcast ram;
  setSkelecog(uint8) required broadcast ram;
  setSkeleRevives(uint8) required broadcast ram;
  setHP(int16) required broadcast ram;
  setElite(uint8) required broadcast ram;
  setMaxHP(uint16) required broadcast ram;
};

dclass DistributedSuit : DistributedSuitBase {
  requestBattle(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) airecv clsend;
  setSPDoId(uint32) required broadcast ram;
  setPathEndpoints(uint16, uint16, uint16, uint16) required broadcast ram;
  setPathPosition(uint16, int16) required broadcast ram;
  setPathState(int8) required broadcast ram;
  debugSuitPosition(int16/10, int16, int16/10, int16/10, int16) broadcast;
};

dclass DistributedTutorialSuit : DistributedSuitBase {
  requestBattle(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) airecv clsend;
};

dclass DistributedFactorySuit : DistributedSuitBase {
  setLevelDoId(uint32) required broadcast ram;
  setCogId(uint32) required broadcast ram;
  setReserve(uint8) required broadcast ram;
  requestBattle(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) airecv clsend;
  setAlert(uint32) airecv clsend;
  setConfrontToon(uint32) broadcast;
  setStrayed() airecv clsend;
  setReturn() broadcast;
};

dclass DistributedMintSuit : DistributedFactorySuit {
};

dclass DistributedBoardOfficeSuit : DistributedFactorySuit {
};

dclass DistributedStageSuit : DistributedFactorySuit {
};

dclass DistributedBossCog : DistributedNode {
  setDNAString(blob) required broadcast db;
  setToonIds(uint32[], uint32[], uint32[]) broadcast ram;
  setBattleIds(uint8, uint32, uint32) broadcast ram;
  setArenaSide(uint8) broadcast ram;
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  avatarNearEnter() airecv clsend;
  avatarNearExit() airecv clsend;
  toonDied(uint32) broadcast;
  setBattleExperience(int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], uint8[], int16[], uint32[]) required broadcast ram;
  zapToon(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10, int8/100, int8/100, uint8, int16) airecv clsend;
  showZapToon(uint32, int16/10, int16/10, int16/10, int16/10, int16/10, int16/10, uint8, int16) broadcast;
  setAttackCode(uint8, uint32) broadcast;
  setHealthTag(string) broadcast ram;
};

dclass DistributedSellbotBoss : DistributedBossCog {
  setCagedToonNpcId(uint32) required broadcast ram;
  setDooberIds(uint32[]) broadcast ram;
  setBossDamage(uint16, uint8, int16) broadcast ram;
  setState(string) broadcast ram;
  hitBoss(uint8) airecv clsend;
  hitBossInsides() airecv clsend;
  hitToon(uint32) airecv clsend;
  finalPieSplat() airecv clsend;
  touchCage() airecv clsend;
  doStrafe(uint8, uint8) broadcast;
  cagedToonBattleThree(uint16, uint32) broadcast;
  toonPromoted(uint8(0-1));
};

dclass DistributedCashbotBoss : DistributedBossCog {
  setState(string) broadcast ram;
  setBossDamage(uint16) broadcast ram;
  setRewardId(uint16) broadcast ram;
  applyReward() airecv clsend;
  setBattleDifficulty(uint8) broadcast ram;
  setMaxHp(uint16) broadcast ram;
  setBonusUnites(uint8) broadcast ram;
};

struct LinkPosition {
  int16/100 x;
  int16/100 y;
  int16/100 z;
};

dclass DistributedCashbotBossCrane : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setState(char, uint32) broadcast ram;
  requestControl() airecv clsend;
  requestFree() airecv clsend;
  clearSmoothing(int8) broadcast clsend;
  setCablePos(uint8, int16/100, uint16%360/100, LinkPosition [3], int16) broadcast clsend;
};

dclass DistributedCashbotBossObject : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setObjectState(char, uint32, uint32) broadcast ram;
  requestGrab() airecv clsend;
  rejectGrab();
  requestDrop() airecv clsend;
  hitFloor() clsend;
  requestFree(int16/10, int16/10, int16/10, uint16%360/100) airecv clsend;
  hitBoss(uint16/255) airecv clsend;
  setX(int16/10) broadcast ram clsend airecv;
  setY(int16/10) broadcast ram clsend airecv;
  setZ(int16/10) broadcast ram clsend airecv;
  setH(int16%360/10) broadcast ram clsend airecv;
  setP(int16%360/10) broadcast ram clsend airecv;
  setR(int16%360/10) broadcast ram clsend airecv;
  setPos : setX, setY, setZ;
  setHpr : setH, setP, setR;
  setPosHpr : setX, setY, setZ, setH, setP, setR;
  setXY : setX, setY;
  setXZ : setX, setZ;
  setXYH : setX, setY, setH;
  setXYZH : setX, setY, setZ, setH;
  setComponentL(uint64) broadcast ram clsend airecv;
  setComponentX(int16/10) broadcast ram clsend airecv;
  setComponentY(int16/10) broadcast ram clsend airecv;
  setComponentZ(int16/10) broadcast ram clsend airecv;
  setComponentH(int16%360/10) broadcast ram clsend airecv;
  setComponentP(int16%360/10) broadcast ram clsend airecv;
  setComponentR(int16%360/10) broadcast ram clsend airecv;
  setComponentT(int16) broadcast ram clsend airecv;
  setSmStop : setComponentT;
  setSmH : setComponentH, setComponentT;
  setSmZ : setComponentZ, setComponentT;
  setSmXY : setComponentX, setComponentY, setComponentT;
  setSmXZ : setComponentX, setComponentZ, setComponentT;
  setSmPos : setComponentX, setComponentY, setComponentZ, setComponentT;
  setSmHpr : setComponentH, setComponentP, setComponentR, setComponentT;
  setSmXYH : setComponentX, setComponentY, setComponentH, setComponentT;
  setSmXYZH : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentT;
  setSmPosHpr : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  setSmPosHprL : setComponentL, setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  clearSmoothing(int8) broadcast clsend;
};

dclass DistributedCashbotBossSafe : DistributedCashbotBossObject {
  setIndex(uint8) required broadcast ram;
  requestInitial() airecv clsend;
};

dclass DistributedCashbotBossGoon : DistributedCashbotBossObject {
  requestBattle(int16/10) airecv clsend;
  requestStunned(int16/10) airecv clsend;
  setVelocity(uint8/10) broadcast ram;
  setHFov(uint8) broadcast ram;
  setAttackRadius(uint8) broadcast ram;
  setStrength(uint8) broadcast ram;
  setGoonScale(uint8/50) broadcast ram;
  setupGoon : setVelocity, setHFov, setAttackRadius, setStrength, setGoonScale;
  setTarget(int16/10, int16/10, uint16%360/100, int16) broadcast ram;
  destroyGoon() broadcast clsend airecv;
};

dclass DistributedBoardbotBoss : DistributedBossCog {
  setCagedToonNpcId(uint32) required broadcast ram;
  setDooberIds(uint32[]) broadcast ram;
  setBossDamage(uint16, uint8, int16) broadcast ram;
  setState(string) broadcast ram;
  hitBoss(uint8) airecv clsend;
  hitBossInsides() airecv clsend;
  hitToon(uint32) airecv clsend;
  finalPieSplat() airecv clsend;
  touchCage() airecv clsend;
  doStrafe(uint8, uint8) broadcast;
  cagedToonBattleThree(uint16, uint32) broadcast;
  toonPromoted(uint8(0-1));
};

dclass DistributedBattleBase : DistributedObject {
  setLevelDoId(uint32) required broadcast ram;
  setBattleCellId(uint32) required broadcast ram;
  setInteractivePropTrackBonus(int8) required broadcast ram;
  setPosition(int16/10, int16/10, int16/10) required broadcast ram;
  setZoneId(uint32) required broadcast ram;
  setInitialSuitPos(int16/10, int16/10, int16/10) required broadcast ram;
  setMembers(uint32[], string, string, string, string, string, uint32[], string, string, string, string, int16) required broadcast ram;
  adjust(int16) broadcast;
  setMovie(int8, uint32[], uint32[], int8, int8, int8, int32, int16[], int16, int16, int16[], int8, int8, int8, int8, int8, int32, int16[], int16, int16, int16[], int8, int8, int8, int8, int8, int32, int16[], int16, int16, int16[], int8, int8, int8, int8, int8, int32, int16[], int16, int16, int16[], int8, int8, int8, int8, int8, int16[], int8, int8, int8, int8, int8, int8, int16[], int8, int8, int8, int8, int8, int8, int16[], int8, int8, int8, int8, int8, int8, int16[], int8, int8, int8) required broadcast ram;
  setChosenToonAttacks(uint32[], int16[], int16[], int32[]) broadcast ram;
  setBattleExperience(int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], int32, int16[], int16[], uint32[], int16[], int16[], int16[], int16[], uint32[], uint8[], int16[], uint32[]) required broadcast ram;
  denyLocalToonJoin();
  setBossBattle(uint8) required broadcast ram;
  setState(string, int16) required broadcast ram;
  faceOffDone() airecv clsend;
  toonRequestJoin(int16/10, int16/10, int16/10) airecv clsend;
  toonRequestRun() airecv clsend;
  toonDied() airecv clsend;
  adjustDone() airecv clsend;
  timeout() airecv clsend;
  movieDone() airecv clsend;
  rewardDone() airecv clsend;
  joinDone(uint32) airecv clsend;
  requestAttack(int8, int8, int32) airecv clsend;
  requestPetProxy(uint32) airecv clsend;
};

dclass DistributedBattle : DistributedBattleBase {
};

dclass DistributedBattleBldg : DistributedBattleBase {
};

dclass DistributedBattleTutorial : DistributedBattle {
};

dclass DistributedLevelBattle : DistributedBattle {
};

dclass DistributedBattleFactory : DistributedLevelBattle {
};

dclass DistributedMintBattle : DistributedLevelBattle {
};

dclass DistributedBoardOfficeBattle : DistributedLevelBattle {
};

dclass DistributedStageBattle : DistributedLevelBattle {
};

dclass DistributedBattleFinal : DistributedBattleBase {
  setBossCogId(uint32) required broadcast ram;
  setBattleNumber(uint8) required broadcast ram;
  setBattleSide(uint8) required broadcast ram;
};

dclass DistributedBoat : DistributedObject {
  setState(string, int16) required broadcast ram;
};

dclass DistributedButterfly : DistributedObject {
  setArea(int16, int16) required broadcast ram;
  setState(int8, uint8, uint8, uint16/10, int16) required broadcast ram;
  avatarEnter() airecv clsend;
};

dclass DistributedMMPiano : DistributedObject {
  requestSpeedUp() airecv clsend;
  requestChangeDirection() airecv clsend;
  setSpeed(int16/1000, uint16/100, int16) broadcast ram;
  playSpeedUp(uint32) broadcast;
  playChangeDirection(uint32) broadcast;
};

dclass DistributedDGFlower : DistributedObject {
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  setHeight(uint8/10) broadcast ram;
};

dclass DistributedFishingPond : DistributedObject {
  hitTarget(uint32) airecv clsend;
  setArea(uint32) required broadcast ram;
};

dclass DistributedFishingTarget : DistributedNode {
  setPondDoId(uint32) required broadcast ram;
  setState(uint8, int16/10, uint16/100, uint16/10, int16) required broadcast ram;
};

dclass DistributedFishingSpot : DistributedObject {
  setPondDoId(uint32) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  requestEnter() airecv clsend;
  rejectEnter();
  requestExit() airecv clsend;
  setOccupied(uint32) broadcast ram;
  doCast(uint8/255, int16/100) airecv clsend;
  sellFish() airecv clsend;
  sellFishComplete(uint8, uint16);
  setMovie(uint8, uint8, uint16, uint16, uint16, uint8/100, int16/100) broadcast ram;
};

dclass DistributedPondBingoManager : DistributedObject {
  setPondDoId(uint32) required broadcast ram;
  updateGameState(uint32, uint8);
  setCardState(uint16, uint8, uint16, uint32);
  setState(string, int16);
  cardUpdate(uint16, uint8, uint8, uint8) airecv clsend;
  enableBingo();
  handleBingoCall(uint16) airecv clsend;
  setJackpot(uint16);
};

dclass DistributedCannon : DistributedObject {
  setEstateId(uint32) required broadcast ram;
  setTargetId(uint32) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setActive(uint8) airecv clsend;
  setActiveState(uint8) broadcast ram;
  requestEnter() airecv clsend;
  requestExit() broadcast;
  setMovie(uint8, uint32) broadcast ram;
  setCannonPosition(int32/100, uint32/100) airecv clsend;
  setCannonLit(int32/100, uint32/100) airecv clsend;
  setFired() airecv clsend;
  setLanded() airecv clsend;
  updateCannonPosition(uint32, int32/100, uint32/100) broadcast ram;
  setCannonWillFire(uint32, int32/100, int32/100, uint32/100, int16) broadcast;
  setCannonExit(uint32) broadcast;
  requestBumperMove(int32/100, int32/100, int32/100) airecv clsend;
  setCannonBumperPos(int32/100, int32/100, int32/100) required broadcast ram;
};

dclass DistributedTarget : DistributedObject {
  setPosition(int16/10, int16/10, int16/10) required broadcast ram;
  setState(uint8, uint32/10, uint8) broadcast;
  setReward(uint32) broadcast;
  setResult(uint32) airecv clsend;
  setBonus(int16/10) airecv clsend;
  setCurPinballScore(uint32, int32, int32) clsend airecv;
  setPinballHiScorer(string) broadcast ram;
  setPinballHiScore(int32) broadcast ram;
};

dclass DistributedMinigame : DistributedObject {
  setParticipants(uint32[]) broadcast ram required;
  setTrolleyZone(uint32) broadcast ram required;
  setStartingVotes(uint16[]) broadcast ram required;
  setMetagameRound(int8) broadcast ram required;
  setDifficultyOverrides(int32, int32) broadcast ram required;
  setAvatarJoined() airecv clsend;
  setAvatarReady() airecv clsend;
  setAvatarExited() airecv clsend;
  requestExit() airecv clsend;
  setGameReady() broadcast;
  setGameStart(int16) broadcast;
  setGameExit() broadcast;
  setGameAbort() broadcast;
  requestSkip() airecv clsend;
  setVoteSkips(uint8) broadcast;
};

dclass DistributedMinigameTemplate : DistributedMinigame {
};

dclass DistributedRaceGame : DistributedMinigame {
  setTimerStartTime(int16) broadcast;
  setAvatarChoice(uint8) airecv clsend;
  setAvatarChose(uint32) broadcast;
  setChancePositions(uint8[]) broadcast;
  setServerChoices(int8[], uint8[], int8[]) broadcast;
};

dclass DistributedCannonGame : DistributedMinigame {
  setCannonPosition(int32/100, uint32/100) airecv clsend;
  setCannonLit(int32/100, uint32/100) airecv clsend;
  updateCannonPosition(uint32, int32/100, uint32/100) broadcast;
  setCannonWillFire(uint32, int32/100, int32/100, uint32/100) broadcast;
  setToonWillLandInWater(int32/100) airecv clsend;
  announceToonWillLandInWater(uint32, int32/100) broadcast;
};

dclass DistributedPhotoGame : DistributedMinigame {
  newClientPhotoScore(uint8, char [0-256], uint32/100) airecv clsend;
  newAIPhotoScore(uint32, uint8, uint32/100) broadcast;
  filmOut() airecv clsend;
};

dclass DistributedPatternGame : DistributedMinigame {
  reportPlayerReady() airecv clsend;
  setPattern(uint8[]) broadcast;
  reportPlayerPattern(uint8[], uint16/1000) airecv clsend;
  setPlayerPatterns(uint8[], uint8[], uint8[], uint8[], uint32) broadcast;
  reportButtonPress(uint8, uint8) airecv clsend;
  remoteButtonPressed(uint32, uint8, uint8) broadcast;
};

dclass DistributedRingGame : DistributedMinigame {
  setTimeBase(int16) broadcast ram required;
  setColorIndices(int8, int8, int8, int8) broadcast ram required;
  setToonGotRing(uint8) airecv clsend;
  setRingGroupResults(uint8) broadcast;
};

dclass DistributedTagGame : DistributedMinigame {
  tag(uint32) airecv clsend;
  setIt(uint32) broadcast;
  setTreasureScore(uint16[]) broadcast;
};

dclass DistributedMazeGame : DistributedMinigame {
  claimTreasure(uint32) airecv clsend;
  setTreasureGrabbed(uint32, uint32) broadcast;
  allTreasuresTaken() broadcast;
  hitBySuit(uint32, int16) clsend broadcast;
};

dclass DistributedTugOfWarGame : DistributedMinigame {
  reportPlayerReady(uint8) airecv clsend;
  sendGoSignal(uint8[]) broadcast;
  sendStopSignal(uint32[], uint32[], uint32[]) broadcast;
  sendGameType(uint8, uint8) broadcast;
  reportEndOfContest(uint8) airecv clsend;
  sendNewAvIdList(uint32[]) airecv clsend;
  reportCurrentKeyRate(uint32, int16/100) airecv clsend;
  sendCurrentPosition(uint32[], int16/1000[]) broadcast;
  sendSuitPosition(int32/1000) broadcast;
  remoteKeyRateUpdate(uint32, uint32) broadcast;
};

dclass DistributedCatchGame : DistributedMinigame {
  claimCatch(uint32, uint32) airecv clsend;
  setObjectCaught(uint32, uint32) broadcast;
  hitBySuit(uint32, int16) clsend broadcast;
  reportDone() airecv clsend;
  setEveryoneDone() broadcast;
};

dclass DistributedDivingGame : DistributedMinigame {
  pickupTreasure(uint32) airecv clsend;
  setTreasureGrabbed(uint32, uint32) broadcast;
  handleFishCollision(uint32, uint32, uint32, char [0-256]) airecv clsend;
  performFishCollision(uint32, uint32, uint32, int16) broadcast;
  handleCrabCollision(uint32, char [0-256]) airecv clsend;
  performCrabCollision(uint32, int16) broadcast;
  setTreasureDropped(uint32, int16) broadcast;
  fishSpawn(int16, uint32, uint32, uint16) broadcast;
  removeFish(uint32) airecv clsend;
  getCrabMoving(uint32, int16, int8) airecv clsend;
  setCrabMoving(uint32, int16, int8, int8, int16, int8) broadcast;
  treasureRecovered() airecv clsend;
  incrementScore(uint32, uint32, int16) broadcast;
};

dclass DistributedTargetGame : DistributedMinigame {
  setTimeBase(int16) broadcast ram required;
  setToonGotRing(uint8) airecv clsend;
  setRingGroupResults(uint8) broadcast;
  setPlayerDone() airecv clsend;
  setScore(int32, int32) airecv clsend;
  setTargetSeed(uint32) broadcast ram;
  setRoundDone() broadcast;
  setSingleScore(uint16, uint32) broadcast;
  setGameDone() broadcast;
};

dclass EstateManager : DistributedObject {
  startAprilFools() broadcast;
  stopAprilFools() broadcast;
  getEstateZone(uint32 avId) airecv clsend;
  setEstateZone(uint32 ownerId, uint32 zoneId);
  setAvHouseId(uint32, uint32[]) broadcast;
  sendAvToPlayground(DoId avId, uint8 reason);
  exitEstate() airecv clsend;
  removeFriend(uint32, uint32) airecv clsend;
};

struct decorItem {
  uint8 decorType;
  uint8 dataByte[];
  uint32 dataWord[];
};

struct lawnItem {
  uint8 type;
  uint8 hardPoint;
  int8 waterLevel;
  int8 growthLevel;
  uint16 optional;
};

dclass DistributedEstate : DistributedObject {
  string DcObjectType db;
  setEstateReady() broadcast;
  setClientReady() airecv clsend;
  setEstateType(uint8 type = 0) required broadcast db;
  setClosestHouse(uint8) airecv clsend;
  setTreasureIds(uint32[]) broadcast ram;
  requestServerTime() airecv clsend;
  setServerTime(uint32);
  setDawnTime(uint32) required broadcast ram;
  placeOnGround(uint32) broadcast ram;
  setDecorData(lawnItem items[] = []) required airecv db;
  setLastEpochTimeStamp(uint32 timestamp = 0) required airecv db;
  setRentalTimeStamp(uint32 timestamp = 0) required airecv db;
  setRentalType(uint8 type = 0) required airecv db;
  setSlot0ToonId(uint32 toonId = 0) required airecv db;
  setSlot0Garden(blob g) required ownrecv db;
  setSlot1ToonId(uint32 toonId = 0) required airecv db;
  setSlot1Garden(blob g) required ownrecv db;
  setSlot2ToonId(uint32 toonId = 0) required airecv db;
  setSlot2Garden(blob g) required ownrecv db;
  setSlot3ToonId(uint32 toonId = 0) required airecv db;
  setSlot3Garden(blob g) required ownrecv db;
  setSlot4ToonId(uint32 toonId = 0) required airecv db;
  setSlot4Garden(blob g) required ownrecv db;
  setSlot5ToonId(uint32 toonId = 0) required airecv db;
  setSlot5Garden(blob g) required ownrecv db;
  setIdList(uint32 []) broadcast ram;
  completeFlowerSale(uint8) airecv clsend;
  awardedTrophy(uint32) broadcast;
  setClouds(uint8) required broadcast ram;
  cannonsOver() broadcast;
  gameTableOver() broadcast;
};

dclass DistributedHouse : DistributedObject {
  string DcObjectType db;
  setHousePos(uint8) required broadcast;
  setHouseType(uint8 type = 0) required broadcast db;
  setGardenPos(uint8 index = 0) required broadcast db;
  setAvatarId(uint32 toonId = 0) required broadcast db;
  setName(string toonName = "") required broadcast db;
  setColor(uint8 colorIndex = 0) required broadcast db;
  setAtticItems(blob = "") required db;
  setInteriorItems(blob = "") required db;
  setAtticWallpaper(blob = "") required db;
  setInteriorWallpaper(blob = "") required db;
  setAtticWindows(blob = "") required db;
  setInteriorWindows(blob = "") required db;
  setDeletedItems(blob = "") required db;
  setInteriorInitialized(uint8 initialized = 0) required db;
  setCannonEnabled(uint8) required;
  setHouseReady() broadcast ram;
  setInteriorLayout(uint8 layoutId = 0) required broadcast db;
};

dclass DistributedHouseInterior : DistributedObject {
  setHouseId(uint32) required broadcast ram;
  setHouseIndex(uint8) required broadcast ram;
  setWallpaper(blob) required broadcast ram;
  setWindows(blob) required broadcast ram;
  setInteriorLayout(uint8) required broadcast ram;
};

dclass DistributedGarden : DistributedObject {
  sendNewProp(uint8, int16/10, int16/10, int16/10) broadcast;
};

dclass DistributedParty : DistributedObject {
  setPartyClockInfo(uint8, uint8, uint8) required broadcast;
  setInviteeIds(uint32[]) required broadcast;
  setPartyState(bool) required broadcast;
  setPartyInfoTuple(party) required broadcast;
  setAvIdsAtParty(uint32 []) required broadcast;
  setPartyStartedTime(string) required broadcast;
  setHostName(string) required broadcast;
  enteredParty() clsend airecv;
};

dclass DistributedPartyActivity : DistributedObject {
  setX(int16/10) broadcast required;
  setY(int16/10) broadcast required;
  setH(uint16%360/100) broadcast required;
  setPartyDoId(uint32) broadcast required;
  toonJoinRequest() airecv clsend;
  toonExitRequest() airecv clsend;
  toonExitDemand() airecv clsend;
  toonReady() airecv clsend;
  joinRequestDenied(uint8);
  exitRequestDenied(uint8);
  setToonsPlaying(uint32 []) broadcast ram;
  setState(string, int16) broadcast ram;
  showJellybeanReward(uint32, uint8, string);
};

dclass DistributedPartyTeamActivity : DistributedPartyActivity {
  toonJoinRequest(uint8(0-1)) airecv clsend;
  toonExitRequest(uint8(0-1)) airecv clsend;
  toonSwitchTeamRequest() airecv clsend;
  setPlayersPerTeam(uint8, uint8) broadcast required;
  setDuration(uint8) broadcast required;
  setCanSwitchTeams(bool) broadcast required;
  setState(string, int16, uint32) broadcast ram;
  setToonsPlaying(uint32 [0-8], uint32 [0-8]) required broadcast ram;
  setAdvantage(uint16/100);
  switchTeamRequestDenied(uint8);
};

struct CatchGeneration {
  uint32 generation;
  uint32 timestamp;
  int8 numPlayers;
};

dclass DistributedPartyCatchActivity : DistributedPartyActivity {
  setStartTimestamp(uint32) required broadcast ram;
  setGenerations(CatchGeneration []) required broadcast ram;
  requestActivityStart() airecv clsend;
  startRequestResponse(uint8);
  claimCatch(uint32, uint32, uint32) airecv clsend;
  setObjectCaught(uint32, uint32, uint32) broadcast;
};

dclass DistributedPartyWinterCatchActivity : DistributedPartyCatchActivity {
};

dclass DistributedPartyCogActivity : DistributedPartyTeamActivity {
  pieThrow(uint32, int32, int32/100, int32/100, int32/100, int32/100, uint8) clsend broadcast;
  pieHitsToon(uint32, int32, int32/100, int32/100, int32/100) clsend broadcast;
  pieHitsCog(uint32, int32, int8(0-2), int32/100, int32/100, int32/100, int32, bool) clsend broadcast airecv;
  setCogDistances(int8/100 [3]) broadcast ram;
  setHighScore(string, uint16) broadcast ram;
};

dclass DistributedPartyWinterCogActivity : DistributedPartyCogActivity {
};

dclass DistributedPartyDanceActivityBase : DistributedPartyActivity {
  updateDancingToon(uint8, char [0-256]) clsend airecv;
  setToonsPlaying(uint32 [], uint16%360/100 []) broadcast ram;
  setDancingToonState(uint32, uint8, string) broadcast;
};

dclass DistributedPartyDanceActivity : DistributedPartyDanceActivityBase {
};

dclass DistributedPartyDance20Activity : DistributedPartyDanceActivityBase {
};

dclass DistributedPartyValentineDanceActivity : DistributedPartyDanceActivityBase {
};

dclass DistributedPartyValentineDance20Activity : DistributedPartyDanceActivityBase {
};

dclass DistributedPartyJukeboxActivityBase : DistributedPartyActivity {
  setNextSong(jukeboxSongInfo) clsend airecv;
  setSongPlaying(jukeboxSongInfo, uint32) broadcast ram;
  queuedSongsRequest() clsend airecv;
  queuedSongsResponse(jukeboxSongInfo [], int16);
  setSongInQueue(jukeboxSongInfo);
  moveHostSongToTopRequest() clsend airecv;
  moveHostSongToTop();
};

dclass DistributedPartyJukeboxActivity : DistributedPartyJukeboxActivityBase {
};

dclass DistributedPartyJukebox40Activity : DistributedPartyJukeboxActivityBase {
};

dclass DistributedPartyValentineJukeboxActivity : DistributedPartyJukeboxActivityBase {
};

dclass DistributedPartyValentineJukebox40Activity : DistributedPartyJukeboxActivityBase {
};

dclass DistributedPartyCannonActivity : DistributedPartyActivity {
  setMovie(uint8, uint32) broadcast;
  setLanded(uint32) airecv broadcast clsend;
  setCannonWillFire(uint32, int32/100, uint32/100) broadcast;
  cloudsColorRequest() clsend airecv;
  cloudsColorResponse(partyCloudColor []);
  requestCloudHit(uint16, uint8/100, uint8/100, uint8/100) clsend airecv;
  setCloudHit(uint16, uint8/100, uint8/100, uint8/100) broadcast;
  setToonTrajectoryAi(int32, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100) airecv clsend;
  setToonTrajectory(uint32, int32, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100, int32/100) broadcast;
  updateToonTrajectoryStartVelAi(int32/100, int32/100, int32/100) airecv clsend;
  updateToonTrajectoryStartVel(uint32, int32/100, int32/100, int32/100) broadcast;
};

dclass DistributedPartyCannon : DistributedObject {
  setActivityDoId(uint64) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  requestEnter() airecv clsend;
  requestExit() broadcast;
  setMovie(uint8, uint32) broadcast ram;
  setCannonPosition(int32/100, uint32/100) airecv clsend;
  setCannonLit(int32/100, uint32/100) airecv clsend;
  setFired() airecv clsend;
  setLanded(uint32) airecv clsend;
  updateCannonPosition(uint32, int32/100, uint32/100) broadcast ram;
  setCannonExit(uint32) broadcast;
  setTimeout() clsend airecv;
};

dclass DistributedPartyFireworksActivity : DistributedPartyActivity {
  setEventId(uint8 eventId) required broadcast;
  setShowStyle(uint8 style) required broadcast;
  setSongId(uint8 songId) required broadcast;
};

dclass DistributedPartyTrampolineActivity : DistributedPartyActivity {
  awardBeans(uint8, uint16) clsend airecv;
  setBestHeightInfo(string, uint16) broadcast ram;
  reportHeightInformation(uint16) airecv clsend;
  leaveTrampoline() broadcast;
  requestAnim(char [0-256]) clsend airecv;
  requestAnimEcho(string) broadcast;
  removeBeans(int8 []) clsend airecv;
  removeBeansEcho(int8 []) broadcast;
};

dclass DistributedPartyValentineTrampolineActivity : DistributedPartyTrampolineActivity {
};

dclass DistributedPartyVictoryTrampolineActivity : DistributedPartyTrampolineActivity {
};

dclass DistributedPartyWinterTrampolineActivity : DistributedPartyTrampolineActivity {
};

dclass DistributedPartyTugOfWarActivity : DistributedPartyTeamActivity {
  reportKeyRateForce(uint32, int16/100) airecv clsend;
  reportFallIn(uint8) airecv clsend;
  setToonsPlaying(uint32 [0-4], uint32 [0-4]) required broadcast ram;
  updateToonKeyRate(uint32, uint32) broadcast;
  updateToonPositions(int16/1000) broadcast;
};

dclass DeleteManager : DistributedObject {
  setInventory(blob) airecv clsend;
};

struct weeklyCalendarHoliday {
  uint8 holidayId;
  uint8 dayOfTheWeek;
};

struct yearlyCalendarHoliday {
  uint8 holidayId;
  uint8[] firstStartTime;
  uint8[] lastEndTime;
};

struct oncelyCalendarHoliday {
  uint8 holidayId;
  uint16[] firstStartTime;
  uint16[] lastEndTime;
};

struct relativelyCalendarHoliday {
  uint8 holidayId;
  uint16[] firstStartTime;
  uint16[] lastEndTime;
};

struct startAndEndTime {
  uint16[] startTime;
  uint16[] endTime;
};

struct multipleStartHoliday {
  uint8 holidayId;
  startAndEndTime times[];
};

dclass NewsManager : DistributedObject {
  setPopulation(uint32) broadcast ram;
  setBingoWin(uint32) broadcast ram;
  setBingoStart() broadcast;
  setBingoOngoing() broadcast;
  setBingoEnd() broadcast;
  setCircuitRaceStart() broadcast;
  setCircuitRaceOngoing() broadcast;
  setCircuitRaceEnd() broadcast;
  setTrolleyHolidayStart() broadcast;
  setTrolleyHolidayOngoing() broadcast;
  setTrolleyHolidayEnd() broadcast;
  setTrolleyWeekendStart() broadcast;
  setTrolleyWeekendOngoing() broadcast;
  setTrolleyWeekendEnd() broadcast;
  setMoreXpHolidayStart() broadcast;
  setMoreXpHolidayOngoing() broadcast;
  setMoreXpHolidayEnd() broadcast;
  setRoamingTrialerWeekendStart() broadcast;
  setRoamingTrialerWeekendOngoing() broadcast;
  setRoamingTrialerWeekendEnd() broadcast;
  setInvasionStatus(uint8, string, uint32, uint8) broadcast;
  setHolidayIdList(uint32[]) broadcast ram;
  holidayNotify() broadcast;
  setWeeklyCalendarHolidays(weeklyCalendarHoliday []) required broadcast ram;
  setYearlyCalendarHolidays(yearlyCalendarHoliday []) required broadcast ram;
  setOncelyCalendarHolidays(oncelyCalendarHoliday []) required broadcast ram;
  setRelativelyCalendarHolidays(relativelyCalendarHoliday []) required broadcast ram;
  setMultipleStartHolidays(multipleStartHoliday []) required broadcast ram;
  sendSystemMessage(string, uint8) broadcast ram;
};

dclass PurchaseManager : DistributedObject {
  setPlayerIds(uint32, uint32, uint32, uint32) required broadcast ram;
  setNewbieIds(uint32[]) required broadcast ram;
  setMinigamePoints(uint8, uint8, uint8, uint8) required broadcast ram;
  setPlayerMoney(uint16, uint16, uint16, uint16) required broadcast ram;
  setPlayerStates(uint8, uint8, uint8, uint8) required broadcast ram;
  setCountdown(int16) required broadcast ram;
  setMetagameRound(int8) required broadcast ram;
  setVotesArray(int16[]) required broadcast ram;
  requestExit() airecv clsend;
  requestPlayAgain() airecv clsend;
  setInventory(blob, int16, uint8) airecv clsend;
  setPurchaseExit() broadcast;
};

dclass NewbiePurchaseManager : PurchaseManager {
  setOwnedNewbieId(uint32) required broadcast ram;
};

dclass SafeZoneManager : DistributedObject {
  enterSafeZone() airecv clsend;
  exitSafeZone() airecv clsend;
};

dclass TutorialManager : DistributedObject {
  requestTutorial() airecv clsend;
  rejectTutorial() airecv clsend;
  requestSkipTutorial() airecv clsend;
  skipTutorialResponse(uint8);
  enterTutorial(uint32, uint32, uint32, uint32);
  allDone() airecv clsend;
  toonArrived() airecv clsend;
};

dclass CatalogManager : DistributedObject {
  startCatalog() airecv clsend;
  fetchPopularItems() airecv clsend;
  setPopularItems(blob);
};

dclass DistributedMyTest : DistributedObject {
  setMyTest(uint16) broadcast;
};

dclass DistributedTreasure : DistributedObject {
  setTreasureType(uint16) required broadcast ram;
  setPosition(int16/10, int16/10, int16/10) required broadcast ram;
  requestGrab() airecv clsend;
  setGrab(uint32) broadcast ram;
  setReject() broadcast;
};

dclass DistributedSZTreasure : DistributedTreasure {
};

dclass DistributedEFlyingTreasure : DistributedSZTreasure {
};

dclass DistributedCashbotBossTreasure : DistributedTreasure {
  setGoonId(uint32) required broadcast ram;
  setFinalPosition(int16/10, int16/10, int16/10) required broadcast ram;
  setStyle(uint16) required broadcast ram;
};

dclass DistributedLargeBlobSender : DistributedObject {
  setMode(uint8) required broadcast ram;
  setTargetAvId(uint32) required broadcast ram;
  setChunk(blob);
  setFilename(string);
  setAck() airecv clsend;
};

dclass DistributedLevel : DistributedObject {
  setLevelZoneId(uint32) required broadcast ram;
  setPlayerIds(uint32[]) required broadcast ram;
  setEntranceId(uint8) required broadcast ram;
  setZoneIds(uint32[]) broadcast ram;
  setStartTimestamp(int32) broadcast ram;
  setOuch(uint8) airecv clsend;
  requestCurrentLevelSpec(string, string) airecv clsend;
  setSpecDeny(blob);
  setSpecSenderDoId(uint32);
  setAttribChange(uint32, blob, blob, blob) broadcast;
};

dclass DistributedEntity : DistributedObject {
  setLevelDoId(uint32) required broadcast ram;
  setEntId(uint32) required broadcast ram;
};

dclass DistributedInteractiveEntity : DistributedEntity {
  setAvatarInteract(uint32) required broadcast ram;
  requestInteract() airecv clsend;
  rejectInteract();
  requestExit() airecv clsend;
  avatarExit(uint32) broadcast;
  setState(string, int32) required broadcast ram;
};

dclass DistributedTrophyMgr : DistributedObject {
  requestTrophyScore() airecv clsend;
};

dclass DistributedBuilding : DistributedObject {
  setBlock(uint16, uint32) required broadcast ram;
  setSuitData(int8, int8, int8) required broadcast ram;
  setVictorList(uint32[]) broadcast ram;
  setState(string, int16) broadcast ram;
  setVictorReady() airecv clsend;
};

dclass DistributedAnimBuilding : DistributedBuilding {
};

dclass DistributedToonInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
  setToonData(blob) required broadcast ram;
  setState(string, int16) required broadcast ram;
  nextSnowmanHeadPart() clsend airecv;
};

dclass DistributedToonHallInterior : DistributedToonInterior {
};

dclass DistributedSuitInterior : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setExtZoneId(uint32) required broadcast ram;
  setDistBldgDoId(uint32) required broadcast ram;
  setNumFloors(int8) required broadcast ram;
  setToons(uint32[], uint16) broadcast ram;
  setSuits(uint32[], uint32[], uint16[]) broadcast ram;
  setState(string, int16) required broadcast ram;
  setAvatarJoined() airecv clsend;
  elevatorDone() airecv clsend;
  reserveJoinDone() airecv clsend;
};

dclass DistributedCogdoBarrel : DistributedObject {
  requestGrab() airecv clsend;
  setIndex(uint32) required broadcast ram;
  setState(uint32) required broadcast ram;
  setGrab(uint32) broadcast ram;
  setReject() broadcast;
};

dclass DistributedCogdoInterior : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setExtZoneId(uint32) required broadcast ram;
  setDistBldgDoId(uint32) required broadcast ram;
  setNumFloors(int8) required broadcast ram;
  setShopOwnerNpcId(uint32) required broadcast ram;
  setSOSNpcId(uint32) broadcast ram;
  setFOType(int8) broadcast ram;
  setToons(uint32[], uint16) broadcast ram;
  setSuits(uint32[], uint32[], uint16[]) broadcast ram;
  setState(string, int16) required broadcast ram;
  setAvatarJoined() airecv clsend;
  elevatorDone() airecv clsend;
  reserveJoinDone() airecv clsend;
  toonLeftBarrelRoom() airecv clsend;
  toonBarrelRoomIntroDone() airecv clsend;
  setBarrelRoomReward(uint32 [], uint8 []) broadcast;
  toonBarrelRoomRewardDone() airecv clsend;
};

dclass DistributedCogdoBattleBldg : DistributedBattleBldg {
};

dclass DistCogdoGame : DistributedObject {
  setInteriorId(uint32) required broadcast ram;
  setExteriorZone(uint32) broadcast ram required;
  setDifficultyOverrides(int32, int32) broadcast ram required;
  setVisible() broadcast;
  setIntroStart() broadcast;
  setToonSad(uint32) broadcast;
  setToonDisconnect(uint32) broadcast;
  setAvatarReady() airecv clsend;
  setGameStart(int16) broadcast;
  setGameFinish(int16) broadcast;
};

dclass DistCogdoLevelGame : DistributedLevel, DistCogdoGame {

};

dclass DistCogdoMazeGame : DistCogdoGame {
  requestAction(uint8, uint32) airecv clsend;
  doAction(uint8, uint32, int16) broadcast;
  setNumSuits(uint8 [3]) required broadcast;
  requestUseGag(int16/10, int16/10, int16/10, int16) clsend airecv;
  toonUsedGag(uint32, int16/10, int16/10, int16/10, int16) broadcast;
  requestSuitHitByGag(uint8, uint8) clsend airecv;
  suitHitByGag(uint32, uint8, uint8) broadcast;
  requestHitBySuit(uint8, uint8, int16) clsend airecv;
  toonHitBySuit(uint32, uint8, uint8, int16) broadcast;
  requestHitByDrop() clsend airecv;
  toonHitByDrop(uint32) broadcast;
  requestPickUp(uint8) clsend airecv;
  pickUp(uint32, uint8, int16) broadcast;
  requestGag(uint8) clsend airecv;
  hasGag(uint32, int16) broadcast;
};

dclass DistCogdoFlyingGame : DistCogdoGame {
  requestAction(uint8, uint8) airecv clsend;
  requestPickUp(uint16, uint8) airecv clsend;
  pickUp(uint32, uint16, int16) broadcast;
  debuffPowerup(uint32, uint16, int16) broadcast;
  doAction(uint8, uint32) broadcast;
  eagleExitCooldown(uint32, int16) broadcast;
  toonSetAsEagleTarget(uint32, uint8, int16) broadcast;
  toonClearAsEagleTarget(uint32, uint8, int16) broadcast;
  toonDied(uint32, int32) broadcast;
  toonSpawn(uint32, int32) broadcast;
  toonSetBlades(uint32, int32) broadcast;
  toonBladeLost(uint32) broadcast;
};

dclass DistCogdoBoardroomGame : DistCogdoLevelGame {
};

dclass DistCogdoCraneGame : DistCogdoLevelGame {
};

dclass DistCogdoCrane : DistributedObject {
  setCraneGameId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setState(char, uint32) broadcast ram;
  clearSmoothing(int8) broadcast clsend;
  setCablePos(uint8, int16/100, uint16%360/100, LinkPosition [3], int16) broadcast clsend;
};

dclass DistCogdoCraneObject : DistributedObject {
  setCraneGameId(uint32) required broadcast ram;
  setObjectState(char, uint32, uint32) broadcast ram;
  requestGrab() airecv clsend;
  rejectGrab();
  requestDrop() airecv clsend;
  hitFloor() clsend;
  requestFree(int16/10, int16/10, int16/10, uint16%360/100) airecv clsend;
  hitBoss(uint16/255) airecv clsend;
  setX(int16/10) broadcast ram clsend airecv;
  setY(int16/10) broadcast ram clsend airecv;
  setZ(int16/10) broadcast ram clsend airecv;
  setH(int16%360/10) broadcast ram clsend airecv;
  setP(int16%360/10) broadcast ram clsend airecv;
  setR(int16%360/10) broadcast ram clsend airecv;
  setPos : setX, setY, setZ;
  setHpr : setH, setP, setR;
  setPosHpr : setX, setY, setZ, setH, setP, setR;
  setXY : setX, setY;
  setXZ : setX, setZ;
  setXYH : setX, setY, setH;
  setXYZH : setX, setY, setZ, setH;
  setComponentL(uint64) broadcast ram clsend airecv;
  setComponentX(int16/10) broadcast ram clsend airecv;
  setComponentY(int16/10) broadcast ram clsend airecv;
  setComponentZ(int16/10) broadcast ram clsend airecv;
  setComponentH(int16%360/10) broadcast ram clsend airecv;
  setComponentP(int16%360/10) broadcast ram clsend airecv;
  setComponentR(int16%360/10) broadcast ram clsend airecv;
  setComponentT(int16) broadcast ram clsend airecv;
  setSmStop : setComponentT;
  setSmH : setComponentH, setComponentT;
  setSmZ : setComponentZ, setComponentT;
  setSmXY : setComponentX, setComponentY, setComponentT;
  setSmXZ : setComponentX, setComponentZ, setComponentT;
  setSmPos : setComponentX, setComponentY, setComponentZ, setComponentT;
  setSmHpr : setComponentH, setComponentP, setComponentR, setComponentT;
  setSmXYH : setComponentX, setComponentY, setComponentH, setComponentT;
  setSmXYZH : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentT;
  setSmPosHpr : setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  setSmPosHprL : setComponentL, setComponentX, setComponentY, setComponentZ, setComponentH, setComponentP, setComponentR, setComponentT;
  clearSmoothing(int8) broadcast clsend;
};

dclass DistCogdoCraneMoneyBag : DistCogdoCraneObject {
  setIndex(uint8) required broadcast ram;
  requestInitial() airecv clsend;
};

dclass DistCogdoCraneCog : DistributedObject {
  setGameId(uint32) required broadcast ram;
  setDNAString(blob) required broadcast ram;
  setSpawnInfo(uint8, int16) required broadcast ram;
};

dclass DistributedHQInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
  setLeaderBoard(blob) required broadcast ram;
  setTutorial(uint8) required broadcast ram;
};

dclass DistributedGagshopInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
};

dclass DistributedPetshopInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
};

dclass DistributedKartShopInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
};

dclass DistributedDoor : DistributedObject {
  setZoneIdAndBlock(uint32, uint32) required broadcast ram;
  setSwing(int8) required broadcast ram;
  setDoorType(uint8) required broadcast ram;
  setDoorIndex(uint8) required broadcast ram;
  setOtherZoneIdAndDoId(uint32, uint32);
  requestEnter() airecv clsend;
  requestExit() airecv clsend;
  rejectEnter(int8);
  avatarEnter(uint32) broadcast;
  avatarExit(uint32) broadcast;
  setState(string, int16) required broadcast ram;
  setExitDoorState(string, int16) required broadcast ram;
};

dclass DistributedAnimDoor : DistributedDoor {
};

dclass DistributedLightSwitch : DistributedObject {
  setInteriorDoId(uint32) required broadcast ram;
  toggleLight() clsend airecv;
  setLightState(bool) broadcast;
};

dclass DistributedHouseDoor : DistributedDoor {
};

dclass DistributedCogHQDoor : DistributedDoor {
};

dclass DistributedSellbotHQDoor : DistributedCogHQDoor {
  informPlayer(uint8) broadcast ram;
};

dclass DistributedNPCToonBase : DistributedNode {
  setName(string) required broadcast ram;
  setDNAString(blob) required broadcast ram;
  setPositionIndex(uint8) required broadcast ram;
  setAnimState(string, int16/1000, int16) broadcast ram;
  setPageNumber(int16, int8, int16) broadcast ram clsend;
  avatarEnter() airecv clsend;
  freeAvatar();
  setHat(uint8 = 0, uint8 = 0, uint8 = 0) broadcast ram;
  setGlasses(uint8 = 0, uint8 = 0, uint8 = 0) broadcast ram;
  setBackpack(uint8 = 0, uint8 = 0, uint8 = 0) broadcast ram;
  setShoes(uint8 = 0, uint8 = 0, uint8 = 0) broadcast ram;
};

dclass DistributedNPCToon : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint16[], int16) broadcast ram;
  setMovieDone() airecv clsend;
  chooseQuest(uint16) airecv clsend;
  chooseTrack(int8) airecv clsend;
};

dclass DistributedNPCHQOfficer : DistributedNPCToon {
};

dclass DistributedNPCSpecialQuestGiver : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint16[], int16) broadcast ram;
  setMovieDone() airecv clsend;
  chooseQuest(uint16) airecv clsend;
  chooseTrack(int8) airecv clsend;
};

dclass DistributedNPCFlippyInToonHall : DistributedNPCToon {
};

dclass DistributedNPCScientist : DistributedNPCToonBase {
  setChat(char [0-1024], uint8, uint32, uint8, uint8) ownsend broadcast;
};

dclass DistributedNPCClerk : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, int16) broadcast ram;
  setInventory(blob, int16, uint8) airecv clsend;
};

dclass DistributedNPCTailor : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, int16) broadcast ram;
  setDNA(blob, int8, uint8) airecv clsend;
  setCustomerDNA(uint32, blob) broadcast ram;
};

dclass DistributedNPCBlocker : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, int16) broadcast ram;
};

dclass DistributedNPCFisherman : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint32[], int16) broadcast ram;
  completeSale(uint8) airecv clsend;
};

dclass DistributedNPCPartyPerson : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint32[], int16) broadcast ram;
  answer(uint8) airecv clsend;
};

dclass DistributedNPCPetclerk : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint32[], int16) broadcast ram;
  setPetSeeds(uint32[]);
  petAdopted(uint8, uint32) airecv clsend;
  petReturned() airecv clsend;
  fishSold() airecv clsend;
  transactionDone() airecv clsend;
};

dclass DistributedNPCKartClerk : DistributedNPCToonBase {
  setMovie(uint8, uint32, uint32, uint32[], int16) broadcast ram;
  buyKart(uint8) airecv clsend;
  buyAccessory(uint8) airecv clsend;
  transactionDone() airecv clsend;
};

dclass DistributedNPCLoopyG : DistributedNPCToon {
};

dclass DistributedNPCInvisible : DistributedNPCToon{
};

dclass DistributedKnockKnockDoor : DistributedAnimatedProp {
};

dclass DistributedElevator : DistributedObject {
  setBldgDoId(uint32) required broadcast ram;
  setState(string, int16) broadcast ram;
  fillSlot0(uint32, uint8) broadcast ram;
  fillSlot1(uint32, uint8) broadcast ram;
  fillSlot2(uint32, uint8) broadcast ram;
  fillSlot3(uint32, uint8) broadcast ram;
  fillSlot4(uint32, uint8) broadcast ram;
  fillSlot5(uint32, uint8) broadcast ram;
  fillSlot6(uint32, uint8) broadcast ram;
  fillSlot7(uint32, uint8) broadcast ram;
  emptySlot0(uint32, int8, int16, int16) broadcast ram;
  emptySlot1(uint32, int8, int16, int16) broadcast ram;
  emptySlot2(uint32, int8, int16, int16) broadcast ram;
  emptySlot3(uint32, int8, int16, int16) broadcast ram;
  emptySlot4(uint32, int8, int16, int16) broadcast ram;
  emptySlot5(uint32, int8, int16, int16) broadcast ram;
  emptySlot6(uint32, int8, int16, int16) broadcast ram;
  emptySlot7(uint32, int8, int16, int16) broadcast ram;
  requestBoard() airecv clsend;
  rejectBoard(uint32, uint8);
  requestExit() airecv clsend;
  setElevatorTripId(uint32) required broadcast ram;
  setAntiShuffle(uint8) required broadcast ram;
  setMinLaff(uint8) required broadcast ram;
};

dclass DistributedElevatorFSM : DistributedObject {
  setBldgDoId(uint32) required broadcast ram;
  setState(string, int16) broadcast ram;
  fillSlot0(uint32) broadcast ram;
  fillSlot1(uint32) broadcast ram;
  fillSlot2(uint32) broadcast ram;
  fillSlot3(uint32) broadcast ram;
  fillSlot4(uint32) broadcast ram;
  fillSlot5(uint32) broadcast ram;
  fillSlot6(uint32) broadcast ram;
  fillSlot7(uint32) broadcast ram;
  emptySlot0(uint32, int8, int16) broadcast ram;
  emptySlot1(uint32, int8, int16) broadcast ram;
  emptySlot2(uint32, int8, int16) broadcast ram;
  emptySlot3(uint32, int8, int16) broadcast ram;
  emptySlot4(uint32, int8, int16) broadcast ram;
  emptySlot5(uint32, int8, int16) broadcast ram;
  emptySlot6(uint32, int8, int16) broadcast ram;
  emptySlot7(uint32, int8, int16) broadcast ram;
  requestBoard() airecv clsend;
  rejectBoard(uint32, uint8);
  requestExit() airecv clsend;
  setElevatorTripId(uint32) required broadcast ram;
  setAntiShuffle(uint8) required broadcast ram;
  setMinLaff(uint8) required broadcast ram;
};

dclass DistributedElevatorFloor : DistributedElevatorFSM {
  setFloor(int8) broadcast ram;
  setLocked(uint16) required broadcast ram;
  setEntering(uint16) required broadcast ram;
  kickToonsOut() broadcast;
  setLatch(uint32) required broadcast ram;
};

dclass DistributedElevatorExt : DistributedElevator {
  setFloor(int8) broadcast ram;
};

dclass DistributedLawOfficeElevatorExt : DistributedElevatorExt {
  setEntranceId(uint8) required broadcast ram;
  setLawOfficeInteriorZone(uint32);
  setLawOfficeInteriorZoneForce(uint32);
};

dclass DistributedElevatorInt : DistributedElevator {
  requestBuildingExit() airecv clsend;
  forcedExit(uint32);
};

dclass DistributedFactoryElevatorExt : DistributedElevatorExt {
  setEntranceId(uint8) required broadcast ram;
  setFactoryInteriorZone(uint32);
  setFactoryInteriorZoneForce(uint32);
};

dclass DistributedMintElevatorExt : DistributedElevatorExt {
  setMintId(uint16) required broadcast ram;
  setMintInteriorZone(uint32);
  setMintInteriorZoneForce(uint32);
};

dclass DistributedBoardOfficeElevatorExt : DistributedElevatorExt {
  setBoardOfficeId(uint16) required broadcast ram;
  setBoardOfficeInteriorZone(uint32);
  setBoardOfficeInteriorZoneForce(uint32);
};

dclass DistributedCogdoElevatorExt : DistributedElevatorExt {
};

dclass DistributedLawOfficeElevatorInt : DistributedElevatorFloor {
  setLawOfficeInteriorZone(uint32);
};

dclass DistributedCogdoElevatorInt : DistributedElevatorInt {
};

dclass DistributedBossElevator : DistributedElevatorExt {
  setBossOfficeZone(uint32);
  setBossOfficeZoneForce(uint32);
};

dclass DistributedVPElevator : DistributedBossElevator {
};

dclass DistributedCFOElevator : DistributedBossElevator {
};

dclass DistributedCJElevator : DistributedBossElevator {
};

dclass DistributedBBElevator : DistributedBossElevator {
};

dclass DistributedCMElevator : DistributedBossElevator {
};

dclass DistributedBoardingParty : DistributedObject {
  postGroupInfo(uint32, uint32[], uint32[], uint32[]) broadcast;
  informDestinationInfo(uint8) clsend airecv;
  postDestinationInfo(uint8) broadcast;
  postInvite(uint32, uint32, bool) broadcast;
  postInviteCanceled() broadcast;
  postKick(uint32) broadcast;
  postKickReject(uint32, uint32, uint32) broadcast;
  postSizeReject(uint32, uint32, uint32) broadcast;
  postInviteAccepted(uint32) broadcast;
  postInviteDelcined(uint32) broadcast;
  postInviteNotQualify(uint32, int8, uint32) broadcast;
  postAlreadyInGroup() broadcast;
  postGroupDissolve(uint32, uint32, uint32 [], uint8) broadcast;
  postMessageAcceptanceFailed(uint32, int8) broadcast;
  postGroupAlreadyFull() broadcast;
  postSomethingMissing() broadcast;
  postRejectBoard(uint32, int8, uint32 [], uint32 []) broadcast;
  postRejectGoto(uint32, int8, uint32 [], uint32 []) broadcast;
  postMessageInvited(uint32, uint32) broadcast;
  postMessageInvitationFailed(uint32) broadcast;
  acceptGoToFirstTime(uint32) broadcast;
  acceptGoToSecondTime(uint32) broadcast;
  rejectGoToRequest(uint32, int8, uint32 [], uint32 []) broadcast;
  requestInvite(uint32) airecv clsend;
  requestCancelInvite(uint32) airecv clsend;
  requestAcceptInvite(uint32, uint32) airecv clsend;
  requestRejectInvite(uint32, uint32) airecv clsend;
  requestKick(uint32) airecv clsend;
  requestLeave(uint32) airecv clsend;
  requestBoard(uint32) airecv clsend;
  requestGoToFirstTime(uint32) airecv clsend;
  requestGoToSecondTime(uint32) airecv clsend;
  setElevatorIdList(uint32[]) required broadcast ram;
  setGroupSize(uint8) required broadcast ram;
};

dclass DistributedTutorialInterior : DistributedObject {
  setZoneIdAndBlock(uint32, uint16) required broadcast ram;
  setTutorialNpcId(uint32) required broadcast ram;
};

dclass DistributedBankMgr : DistributedObject {
  transferMoney(int16 amount) airecv clsend;
};

dclass DistributedMailbox : DistributedObject {
  setHouseId(uint32) required broadcast ram;
  setHousePos(uint8) required broadcast ram;
  setName(string) required broadcast ram;
  setFullIndicator(uint8) broadcast ram;
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  freeAvatar();
  setMovie(uint8, uint32) broadcast ram;
  acceptItemMessage(uint16, blob, uint8, int32) airecv clsend;
  acceptItemResponse(uint16, int8);
  discardItemMessage(uint16, blob, uint8, int32) airecv clsend;
  discardItemResponse(uint16, int8);
  acceptInviteMessage(uint16, uint64) airecv clsend;
  rejectInviteMessage(uint16, uint64) airecv clsend;
  markInviteReadButNotReplied(uint64) airecv clsend;
};

dclass DistributedFurnitureManager : DistributedObject {
  setOwnerId(uint32 ownerId) required broadcast ram;
  setOwnerName(string ownerName) required broadcast ram;
  setInteriorId(uint32 interiorId) required broadcast ram;
  setAtticItems(blob atticItems) required broadcast ram;
  setAtticWallpaper(blob atticWallpaper) required broadcast ram;
  setAtticWindows(blob atticWindows) required broadcast ram;
  setDeletedItems(blob deletedItems) required broadcast ram;
  suggestDirector(uint32 directorId) airecv clsend;
  setDirector(uint32 directorId) broadcast ram;
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  moveItemToAtticMessage(uint32 doId, uint16 context) airecv clsend;
  moveItemToAtticResponse(int8 retval, uint16 context);
  moveItemFromAtticMessage(uint16 index, int16/10 x, int16/10 y, int16/100 z, int16/10 h, int16/10 p, int16/10 r, uint16 context) airecv clsend;
  moveItemFromAtticResponse(int8 retval, uint32 doId, uint16 context);
  deleteItemFromAtticMessage(blob item, uint16 index, uint16 context) airecv clsend;
  deleteItemFromAtticResponse(int8 retval, uint16 context);
  deleteItemFromRoomMessage(blob item, uint32 doId, uint16 context) airecv clsend;
  deleteItemFromRoomResponse(int8 retval, uint16 context);
  moveWallpaperFromAtticMessage(uint16 index, uint8 room, uint16 context) airecv clsend;
  moveWallpaperFromAtticResponse(int8 retval, uint16 context);
  deleteWallpaperFromAtticMessage(blob item, uint16 index, uint16 context) airecv clsend;
  deleteWallpaperFromAtticResponse(int8 retval, uint16 context);
  moveWindowToAtticMessage(uint8 slot, uint16 context) airecv clsend;
  moveWindowToAtticResponse(int8 retval, uint16 context);
  moveWindowFromAtticMessage(uint16 index, uint8 slot, uint16 context) airecv clsend;
  moveWindowFromAtticResponse(int8 retval, uint16 context);
  moveWindowMessage(uint8 fromSlot, uint8 toSlot, uint16 context) airecv clsend;
  moveWindowResponse(int8 retval, uint16 context);
  deleteWindowFromAtticMessage(blob item, uint16 index, uint16 context) airecv clsend;
  deleteWindowFromAtticResponse(int8 retval, uint16 context);
  recoverDeletedItemMessage(blob item, uint16 index, uint16 context) airecv clsend;
  recoverDeletedItemResponse(int8 retval, uint16 context);
};

dclass DistributedFurnitureItem : DistributedSmoothNode {
  setItem(uint32 furnitureMgrId, blob item) required broadcast ram;
  requestPosHpr(uint8 final, int16/10 x, int16/10 y, int16/100 z, int16/10 h, int16/10 p, int16/10 r, int16 t) airecv clsend;
  setMode(uint8 mdoe, uint32 avId) required broadcast ram;
};

dclass DistributedBank : DistributedFurnitureItem {
  avatarEnter() airecv clsend;
  freeAvatar();
  setMovie(uint8 mode, uint32 avId, int16 timestamp) broadcast ram;
  transferMoney(int16 amount) airecv clsend;
};

dclass DistributedCloset : DistributedFurnitureItem {
  setOwnerId(uint32) required broadcast ram;
  enterAvatar() airecv clsend;
  freeAvatar();
  removeItem(blob, uint8) airecv clsend;
  setDNA(blob, int8, uint8) airecv clsend;
  setState(uint8, uint32, uint32, string, uint8[], uint8[]) broadcast ram;
  setMovie(uint8, uint32, int16) broadcast ram;
  resetItemLists() broadcast ram;
  setCustomerDNA(uint32, blob) broadcast ram;
};

dclass DistributedTrunk : DistributedCloset {
  setState(uint8, uint32, uint32, string, uint8[], uint8[], uint8[], uint8[]) broadcast ram;
  removeItem(uint8, uint8, uint8, uint8) airecv clsend;
  setDNA(uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, int8, uint8) airecv clsend;
  setCustomerDNA(uint32, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8, uint8) broadcast ram;
};

dclass DistributedPhone : DistributedFurnitureItem {
  setInitialScale(uint8/170, uint8/170, uint8/170) required broadcast ram;
  setNewScale(uint8/170, uint8/170, uint8/170) airecv clsend;
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  freeAvatar();
  setLimits(uint16);
  setMovie(uint8, uint32, int32) broadcast ram;
  requestPurchaseMessage(uint16, blob, int32) airecv clsend;
  requestPurchaseResponse(uint16, int8);
  requestGiftPurchaseMessage(uint16, uint32, blob, int32) airecv clsend;
  requestGiftPurchaseResponse(uint16, int8);
  purchaseItemComplete();
};

dclass DistributedFireworkShow : DistributedObject {
  startShow(uint8, uint8, uint8, int16) broadcast ram;
  requestFirework(int16/10, int16/10, int16/100, uint8, uint8, uint8) airecv clsend;
  shootFirework(int16/10, int16/10, int16/100, uint8, uint8, uint8) broadcast;
};

dclass DistributedFireworksCannon : DistributedFireworkShow {
  avatarEnter() airecv clsend;
  avatarExit() airecv clsend;
  freeAvatar();
  setMovie(uint8, uint32, int16) broadcast ram;
  setPosition(int16/10, int16/10, int16/10) required broadcast ram;
};

dclass LobbyManager : DistributedObject {
};

dclass DistributedFactory : DistributedLevel {
  setFactoryId(uint16) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  setForemanConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
};

dclass DistributedLawOffice : DistributedObject {
  setLawOfficeId(uint16) required broadcast ram;
  startSignal() broadcast ram;
  readyForNextFloor() airecv clsend;
};

dclass DistributedLawOfficeFloor : DistributedLevel {
  setLawOfficeId(uint16) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  readyForNextFloor() airecv clsend;
  setForemanConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
};

dclass DistributedMint : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setMintId(uint16) required broadcast ram;
  setFloorNum(uint8) required broadcast ram;
  setRoomDoIds(uint32[]) broadcast ram;
};

dclass DistributedBoardOffice : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setBoardOfficeId(uint16) required broadcast ram;
  setFloorNum(uint8) required broadcast ram;
  setRoomDoIds(uint32[]) broadcast ram;
};

dclass DistributedMintRoom : DistributedLevel {
  setMintId(uint16) required broadcast ram;
  setRoomId(uint16) required broadcast ram;
  setRoomNum(uint8) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  setBossConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
};
dclass DistributedBoardOfficeRoom : DistributedLevel {
  setBoardOfficeId(uint16) required broadcast ram;
  setRoomId(uint16) required broadcast ram;
  setRoomNum(uint8) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  setBossConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
};

dclass DistributedStage : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setStageId(uint16) required broadcast ram;
  setLayoutIndex(uint16) required broadcast ram;
  setFloorNum(uint8) required broadcast ram;
  setRoomDoIds(uint32[]) broadcast ram;
  setStageZone(uint32) broadcast ram;
  elevatorAlert(uint32) broadcast ram;
};

dclass DistributedStageRoom : DistributedLevel {
  setStageId(uint16) required broadcast ram;
  setRoomId(uint16) required broadcast ram;
  setRoomNum(uint8) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  setBossConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
};

dclass DistributedInGameEditor : DistributedObject {
  setEditorAvId(uint32) required broadcast ram;
  setEditUsername(blob) required broadcast ram;
  setLevelDoId(uint32) required broadcast ram;
  requestCurrentLevelSpec() airecv clsend;
  setSpecSenderDoId(uint32);
  setEdit(uint32, blob, blob, blob) airecv clsend;
  setAttribChange(uint32, blob, blob, blob);
  setFinished() airecv clsend;
};

dclass DistributedLift : DistributedEntity {
  setStateTransition(uint8, uint8, uint32) required broadcast ram;
  setAvatarEnter() airecv clsend;
  setAvatarLeave() airecv clsend;
};

dclass DistributedDoorEntity : DistributedEntity {
  setLocksState(uint16[]) required broadcast ram;
  setDoorState(uint8, int32) required broadcast ram;
  requestOpen() airecv clsend;
};

dclass DistributedSwitch : DistributedInteractiveEntity {
};

dclass DistributedButton : DistributedSwitch {
};

dclass DistributedTrigger : DistributedSwitch {
};

dclass DistributedCrushableEntity : DistributedEntity {
  setPosition(int16/10, int16/10, int16/10) broadcast ram;
  setCrushed(uint32, uint8) broadcast ram;
};

dclass DistributedCrusherEntity : DistributedEntity {
};

dclass DistributedElevatorMarker : DistributedEntity {
};

dclass DistributedStomper : DistributedCrusherEntity {
  setMovie(uint8, int16, uint32[]) broadcast ram;
};

dclass DistributedStomperPair : DistributedEntity {
  setChildren(uint32[]) broadcast ram;
  setSquash() airecv clsend;
};

dclass DistributedBarrelBase : DistributedEntity {
  requestGrab() airecv clsend;
  setGrab(uint32) broadcast ram;
  setReject() broadcast;
};

dclass DistributedGagBarrel : DistributedBarrelBase {
};

dclass DistributedBeanBarrel : DistributedBarrelBase {
};

dclass DistributedHealBarrel : DistributedBarrelBase {
};

dclass DistributedGrid : DistributedEntity {
};

dclass ActiveCell : DistributedEntity {
  setState(uint8, uint32) broadcast ram;
};

dclass DirectionalCell : ActiveCell {
};

dclass CrusherCell : ActiveCell {
};

dclass DistributedCrate : DistributedCrushableEntity {
  requestPush(uint8) airecv clsend;
  setReject();
  setAccept() broadcast;
  setMoveTo(uint32, int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) broadcast ram;
  setDone() airecv clsend;
};

dclass DistributedSinkingPlatform : DistributedEntity {
  setOnOff(uint8, uint32) airecv clsend;
  setSinkMode(uint32, uint8, uint32) broadcast ram;
};

dclass DistributedGoon : DistributedCrushableEntity {
  requestBattle(int16/10) airecv clsend;
  requestStunned(int16/10) airecv clsend;
  requestResync() airecv clsend;
  setParameterize(int16/10, int16/10, int16/10, uint32) airecv clsend;
  setMovie(uint8, uint32, int32/10, int16) broadcast ram;
};

dclass DistributedGridGoon : DistributedGoon {
  setPathPts(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) broadcast ram;
};

dclass BattleBlocker : DistributedEntity {
  setActive(uint8) required broadcast ram;
  setSuits(uint32[]) broadcast ram;
  setBattle(uint32) broadcast ram;
  setBattleFinished() broadcast ram;
};

dclass DistributedLaserField : BattleBlocker {
  setGrid(uint8, uint8) required broadcast ram;
  setField(uint8 []) required broadcast ram;
  setSuccess(uint8) broadcast ram;
  hit(int8, int8, int8, int8) airecv clsend;
  trapFire() airecv clsend;
  setActiveLF(uint8) broadcast ram;
  hideSuit(uint32[]) broadcast ram;
  showSuit(uint32[]) broadcast ram;
  setGridGame(string) broadcast ram;
};

struct golfGreenGameBoardData {
  uint8 posX;
  uint8 posZ;
  uint8 typeIndex;
};

struct golfGreenGameScoreData {
  uint32 avId;
  uint8 score;
};

dclass DistributedGolfGreenGame : BattleBlocker {
  requestJoin() airecv clsend;
  leaveGame() airecv clsend;
  acceptJoin(uint16, int32, uint32 []) broadcast ram;
  requestBoard(uint8) airecv clsend;
  startBoard(golfGreenGameBoardData [], uint8 []);
  signalDone(uint8) broadcast ram;
  boardCleared(uint32);
  scoreData(uint8, uint8, golfGreenGameScoreData []) broadcast ram;
  informGag(uint8, uint8);
  helpOthers(uint32) broadcast;
  setTimerStart(uint16, int32) broadcast ram;
};

dclass DistributedSecurityCamera : DistributedEntity {
  trapFire() airecv clsend;
  setTarget(uint8) broadcast ram;
};

dclass DistributedMover : DistributedEntity {
  startMove(int16) broadcast ram;
};

typedef uint16/10000 PetTrait;

dclass DistributedPet : DistributedSmoothNode {
  string DcObjectType db;
  setOwnerId(uint32) required broadcast db;
  setPetName(string) required broadcast db;
  setTraitSeed(uint32) required broadcast db;
  setSafeZone(uint32) required broadcast db;
  setForgetfulness(PetTrait) required broadcast db;
  setBoredomThreshold(PetTrait) required broadcast db;
  setRestlessnessThreshold(PetTrait) required broadcast db;
  setPlayfulnessThreshold(PetTrait) required broadcast db;
  setLonelinessThreshold(PetTrait) required broadcast db;
  setSadnessThreshold(PetTrait) required broadcast db;
  setFatigueThreshold(PetTrait) required broadcast db;
  setHungerThreshold(PetTrait) required broadcast db;
  setConfusionThreshold(PetTrait) required broadcast db;
  setExcitementThreshold(PetTrait) required broadcast db;
  setAngerThreshold(PetTrait) required broadcast db;
  setSurpriseThreshold(PetTrait) required broadcast db;
  setAffectionThreshold(PetTrait) required broadcast db;
  setHead(int8(-1 - 1)) required broadcast db; // Supposed to be -1 - 0, but minification causes this to become -1-0, which is a parse problem.
  setEars(int8(-1 - 4)) required broadcast db;
  setNose(int8(-1 - 3)) required broadcast db;
  setTail(int8(-1 - 6)) required broadcast db;
  setBodyTexture(int8(0-6)) required broadcast db;
  setColor(int8(0-25)) required broadcast db;
  setColorScale(int8(0-8)) required broadcast db;
  setEyeColor(int8(0-5)) required broadcast db;
  setGender(int8(0-1)) required broadcast db;
  setLastSeenTimestamp(uint32) required broadcast db;
  setBoredom(uint16/1000(0-1)) required broadcast db;
  setRestlessness(uint16/1000(0-1)) required broadcast db;
  setPlayfulness(uint16/1000(0-1)) required broadcast db;
  setLoneliness(uint16/1000(0-1)) required broadcast db;
  setSadness(uint16/1000(0-1)) required broadcast db;
  setAffection(uint16/1000(0-1)) required broadcast db;
  setHunger(uint16/1000(0-1)) required broadcast db;
  setConfusion(uint16/1000(0-1)) required broadcast db;
  setExcitement(uint16/1000(0-1)) required broadcast db;
  setFatigue(uint16/1000(0-1)) required broadcast db;
  setAnger(uint16/1000(0-1)) required broadcast db;
  setSurprise(uint16/1000(0-1)) required broadcast db;
  setMood : setBoredom, setRestlessness, setPlayfulness, setLoneliness, setSadness, setAffection, setHunger, setConfusion, setExcitement, setFatigue, setAnger, setSurprise;
  teleportIn(int16) broadcast ownsend;
  teleportOut(int16) broadcast ownsend;
  setTrickAptitudes(uint16/10000(0-1) []) required broadcast db;
  doTrick(uint8, int16) broadcast ram;
  avatarInteract(uint32);
  setMovie(uint8, uint32, int16) broadcast ram;
  freeAvatar();
};

dclass DistributedPetProxy : DistributedPet {
  setDominantMood(string) broadcast ram;
};

dclass DistributedPublicPet : DistributedPet {
 beginPublicDisplay() broadcast;
 finishPublicDisplay() broadcast;
 sphereEntered() clsend airecv;
 sphereLeft() clsend airecv;
};

dclass DistributedPublicPetMgr : DistributedObject {
 requestAppearance() clsend airecv;
 requestAppearanceResp(uint8);
};

dclass DistributedAprilToonsMgr : DistributedObject {
  setEventActive(uint8 eventId, bool) broadcast;
  requestEventsList() clsend airecv;
  requestEventsListResp(uint8 []);
};

dclass DistributedBlackCatMgr : DistributedObject {
  doBlackCatTransformation(uint32 avId) broadcast;
  requestBlackCatTransformation() airecv clsend;
};

dclass DistributedPolarBearMgr : DistributedObject {
  doPolarBearTransformation(uint32 avId) broadcast;
  requestPolarBearTransformation() airecv clsend;
};

dclass DistributedPolarPlaceEffectMgr : DistributedObject {
  addPolarPlaceEffect() airecv clsend;
};

dclass DistributedSofieListenerMgr : DistributedObject {
  addAchievement() airecv clsend;
};

dclass DistributedGreenToonEffectMgr : DistributedObject {
  addGreenToonEffect() airecv clsend;
};

dclass DistributedResistanceEmoteMgr : DistributedObject {
  addResistanceEmote() clsend airecv;
};

dclass DistributedScavengerHuntTarget : DistributedObject {
  attemptScavengerHunt() airecv clsend;
};

dclass DistributedTrickOrTreatTarget : DistributedObject {
  doScavengerHunt(int8);
  requestScavengerHunt() airecv clsend;
};

dclass DistributedWinterCarolingTarget : DistributedObject {
  doScavengerHunt(int8) broadcast;
  requestScavengerHunt() airecv clsend;
};

dclass DistributedDataStoreManager : DistributedObject {
  startStore(uint8);
  stopStore(uint8);
  queryStore(uint8, string);
  receiveResults(uint8, string);
  deleteBackupStores();
};

dclass DistributedVehicle : DistributedSmoothNode {
  setOwner(uint32) required broadcast ram;
  setState(char, uint32) broadcast ram;
  setBodyType(int8) required broadcast ram;
  setBodyColor(int8) required broadcast ram;
  setAccessoryColor(int8) required broadcast ram;
  setEngineBlockType(int8) required broadcast ram;
  setSpoilerType(int8) required broadcast ram;
  setFrontWheelWellType(int8) required broadcast ram;
  setBackWheelWellType(int8) required broadcast ram;
  setRimType(int8) required broadcast ram;
  setDecalType(int8) required broadcast ram;
  requestControl() airecv clsend;
  requestParked() airecv clsend;
  setInput(int8) broadcast ram;
};

struct avatarAndKart {
  uint32 avId;
  uint32 kartId;
};

dclass DistributedRace : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setTrackId(uint16) required broadcast ram;
  setRaceType(uint16) required broadcast ram;
  setCircuitLoop(uint16[]) required broadcast ram;
  setAvatars(uint32[]) required broadcast ram;
  setStartingPlaces(uint8[]) required broadcast ram;
  setLapCount(uint8) broadcast required ram;
  waitingForJoin() broadcast ram;
  setEnteredRacers(avatarAndKart []) broadcast ram;
  prepForRace() broadcast ram;
  startTutorial() broadcast ram;
  startRace(int16) broadcast ram;
  goToSpeedway(uint32[], uint8) broadcast ram;
  genGag(uint8, uint16, uint8) broadcast ram;
  dropAnvilOn(uint32, uint32, int16) broadcast ram;
  shootPiejectile(uint32, uint32, uint8) broadcast ram;
  racerDisconnected(uint32) broadcast ram;
  setPlace(uint32, uint32/1000, uint8, uint32, uint8, uint32, uint32, uint32[], uint16[], uint32/1000) broadcast ram;
  setCircuitPlace(uint32, uint8, uint32, uint32, uint32, uint32[]) broadcast ram;
  endCircuitRace() broadcast ram;
  setRaceZone(uint32, uint32);
  hasGag(uint8, uint8, uint8) broadcast airecv clsend;
  racerLeft(uint32) clsend airecv broadcast ram;
  heresMyT(uint32, int8, uint16/65535, int16) clsend airecv broadcast;
  requestThrow(int32/1000, int32/1000, int32/1000) clsend airecv;
  requestKart() clsend airecv;
};

dclass DistributedGag : DistributedObject {
  setInitTime(int16) required broadcast ram;
  setActivateTime(int16) required broadcast ram;
  setPos(int32/1000, int32/1000, int32/1000) required broadcast ram;
  setRace(uint32) required broadcast ram;
  setOwnerId(uint32) required broadcast ram;
  setType(uint8) required broadcast ram;
  hitSomebody(uint32, int16) broadcast clsend airecv;
};

dclass DistributedProjectile : DistributedObject {
  setInitTime(int16) required broadcast ram;
  setPos(int32/1000, int32/1000, int32/1000) required broadcast ram;
  setRace(uint32) required broadcast ram;
  setOwnerId(uint32) required broadcast ram;
  setType(uint8) required broadcast ram;
  hitSomebody(uint32, int16) broadcast clsend airecv;
};

dclass DistributedKartPad : DistributedObject {
  setArea(uint32) required broadcast ram;
};

dclass DistributedRacePad : DistributedKartPad {
  setState(string, int16) required broadcast ram;
  setRaceZone(uint32);
  setTrackInfo(uint16[]) required broadcast ram;
};

dclass DistributedViewPad : DistributedKartPad {
  setLastEntered(int16) required broadcast ram;
};

dclass DistributedStartingBlock : DistributedObject {
  setPadDoId(uint32) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setPadLocationId(uint8) required broadcast ram;
  requestEnter(uint8) airecv clsend;
  rejectEnter(uint8);
  requestExit() airecv clsend;
  setOccupied(uint32) broadcast ram;
  setMovie(uint8) broadcast ram;
  movieFinished() airecv clsend;
};

dclass DistributedViewingBlock : DistributedStartingBlock {
};

dclass DistributedLeaderBoard : DistributedObject {
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setDisplay(blob) broadcast ram;
};

dclass DistributedDeliveryManager : DistributedObject {
  hello(string) clsend;
  rejectHello(string);
  helloResponse(string);
  getName(uint32);
  receiveRejectGetName(string);
  receiveAcceptGetName(string);
  addName(uint32, string);
  receiveRejectAddName(uint32);
  receiveAcceptAddName(uint32);
  addGift(uint32, blob, uint32, uint32, uint32);
  receiveRejectAddGift(uint32);
  receiveAcceptAddGift(uint32, uint32, uint32, uint32);
  deliverGifts(uint32, uint32);
  receiveAcceptDeliverGifts(uint32, string);
  receiveRejectDeliverGifts(uint32, string);
  receiveRequestPayForGift(blob, uint32, uint32) airecv clsend;
  receiveRequestPurchaseGift(blob, uint32, uint32, uint32) airecv;
  receiveAcceptPurchaseGift(uint32, uint32, int16);
  receiveRejectPurchaseGift(uint32, uint32, int16, uint16);
  heartbeat() airecv;
  giveBeanBonus(uint32, uint16);
  requestAck() clsend;
  returnAck();
  givePartyRefund(uint32, uint32, uint64, int8, uint16);
};

dclass DistributedLawbotBoss : DistributedBossCog {
  setState(string) broadcast ram;
  setBossDamage(uint16, uint8, int16) broadcast ram;
  touchWitnessStand() airecv clsend;
  hitBoss(uint8) airecv clsend;
  healBoss(uint8) airecv clsend;
  hitToon(uint32) airecv clsend;
  hitDefensePan() airecv clsend;
  hitProsecutionPan() airecv clsend;
  hitChair(uint8, uint8) airecv clsend;
  setLawyerIds(uint32[]) broadcast ram;
  setTaunt(int8, int8) broadcast;
  toonGotHealed(uint32) broadcast;
  enteredBonusState() broadcast;
  setBattleDifficulty(uint8) broadcast ram;
};

dclass DistributedLawbotBossSuit : DistributedSuitBase {
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  doAttack(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) broadcast;
  doProsecute() broadcast;
  hitByToon() airecv clsend;
  doStun() broadcast;
};

dclass DistributedLawbotBossGavel : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setState(char) broadcast ram;
};

dclass DistributedLawbotCannon : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  requestEnter() airecv clsend;
  setMovie(int8, uint32, uint8) broadcast;
  setCannonPosition(int16/10, int16/10) airecv clsend;
  updateCannonPosition(uint32, int16/10, int16/10) broadcast;
  setCannonLit(int16/10, int16/10) airecv clsend;
  setCannonWillFire(uint32, int16/10, int16/10, int16/10, int16) broadcast;
  setLanded() airecv clsend;
  requestLeave() airecv clsend;
};

dclass DistributedLawbotChair : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setState(char) broadcast ram;
  showCogJurorFlying() broadcast;
  setToonJurorIndex(int8) broadcast ram;
};

dclass DistributedLawnDecor : DistributedNode {
  setPlot(int8) required broadcast ram;
  setHeading(int16/10) required broadcast ram;
  setOwnerIndex(int8) required broadcast ram;
  setPosition(int16/10, int16/10, int16/10) required broadcast ram;
  plotEntered() airecv clsend;
  removeItem() airecv clsend;
  setMovie(uint8, uint32) broadcast ram;
  movieDone() airecv clsend;
  interactionDenied(uint32) broadcast ram;
  setBoxDoId(uint32, uint8) broadcast ram;
};

dclass DistributedGardenPlot : DistributedLawnDecor {
  plantFlower(uint8, uint8) airecv clsend;
  plantGagTree(uint8, uint8) airecv clsend;
  plantStatuary(uint8) airecv clsend;
  plantToonStatuary(uint8, uint16) airecv clsend;
  plantNothing(uint8) airecv clsend;
};

dclass DistributedGardenBox : DistributedLawnDecor {
  setTypeIndex(uint8) required broadcast ram;
};

dclass DistributedStatuary : DistributedLawnDecor {
  setTypeIndex(uint8) required broadcast ram;
  setWaterLevel(int8) required broadcast ram;
  setGrowthLevel(int8) required broadcast ram;
};

dclass DistributedToonStatuary : DistributedStatuary {
  setOptional(uint16) required broadcast ram;
};

dclass DistributedAnimatedStatuary : DistributedStatuary {
};

dclass DistributedChangingStatuary : DistributedStatuary {
  setGrowthLevel(int8) required broadcast ram;
};

dclass DistributedPlantBase : DistributedLawnDecor {
  setTypeIndex(uint8) required broadcast ram;
  setWaterLevel(int8) required broadcast ram;
  setGrowthLevel(int8) required broadcast ram;
  waterPlant() airecv clsend;
  waterPlantDone() airecv clsend;
};

dclass DistributedFlower : DistributedPlantBase {
  setTypeIndex(uint8) required broadcast ram;
  setVariety(uint8) required broadcast ram;
};

dclass DistributedGagTree : DistributedPlantBase {
  setWilted(int8) required broadcast ram;
  requestHarvest() airecv clsend;
  setFruiting(bool) required broadcast ram;
};

dclass DistributedTravelGame : DistributedMinigame {
  setTimerStartTime(int16) broadcast;
  setAvatarChoice(uint16, uint8) airecv clsend;
  setAvatarVotes(uint32, uint16) broadcast;
  setAvatarChose(uint32) broadcast;
  setServerChoices(int16[], uint8[], uint8, uint8) broadcast;
  setMinigames(uint8[], uint8[]) broadcast;
  setBonuses(uint8[], uint8[]) broadcast;
  setBoardIndex(uint8) required broadcast ram;
};

dclass DistributedPairingGame : DistributedMinigame {
  setDeckSeed(uint32) required broadcast ram;
  setMaxOpenCards(uint8) broadcast ram;
  openCardRequest(int16, int16) airecv clsend;
  openCardResult(int16, uint32, int16, int8, int16[]) broadcast;
  reportDone() airecv clsend;
  setEveryoneDone() broadcast;
  setSignaling(uint32) clsend broadcast;
};

struct golfData {
  int16 frame;
  int32/100000 x;
  int32/100000 y;
  int32/100000 z;
};

struct Coord3 {
  int32/100000 x;
  int32/100000 y;
  int32/100000 z;
};

struct CommonObjectData {
  uint8 id;
  uint8 type;
  int32/100000 x;
  int32/100000 y;
  int32/100000 z;
  int32/100000 q1;
  int32/100000 q2;
  int32/100000 q3;
  int32/100000 q4;
  int32/100000 aVX;
  int32/100000 aVY;
  int32/100000 aVZ;
  int32/100000 lVX;
  int32/100000 lVY;
  int32/100000 lVZ;
};

dclass DistributedPhysicsWorld : DistributedObject {
  clientCommonObject(uint8, uint8, Coord3, Coord3, int32/100, int32/100, int32/1000) broadcast ram;
  setCommonObjects(CommonObjectData []) broadcast;
  upSetCommonObjects(CommonObjectData []) airecv clsend;
};

dclass DistributedGolfHole : DistributedPhysicsWorld {
  setHoleId(int8) broadcast ram required;
  setTimingCycleLength(uint32/1000) broadcast ram required;
  setAvatarReadyHole() airecv clsend;
  setGolfCourseDoId(uint32) broadcast ram required;
  turnDone() airecv clsend;
  ballInHole() airecv clsend;
  setAvatarTempTee(uint32, uint8) clsend broadcast;
  setTempAimHeading(uint32, int32/1000) clsend broadcast;
  setAvatarFinalTee(uint32, uint8) broadcast;
  setGolferIds(uint32[]) broadcast ram required;
  golfersTurn(uint32) broadcast;
  golferChooseTee(uint32) broadcast;
  setAvatarTee(uint8) airecv clsend;
  postSwing(uint32/1000, int32, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000) airecv clsend;
  postSwingState(uint32/1000, int32, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, uint16/100, CommonObjectData []) airecv clsend;
  swing(uint32, int32, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000) broadcast;
  ballMovie2AI(uint32/1000, uint32, golfData [], golfData [], uint16, uint16, uint16, CommonObjectData []) airecv clsend;
  ballMovie2Client(uint32/1000, uint32, golfData [], golfData [], uint16, uint16, uint16, CommonObjectData []) broadcast;
  assignRecordSwing(uint32, uint32/1000, int32, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, CommonObjectData []);
  setBox(int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000) airecv clsend;
  sendBox(int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000, int32/1000) broadcast;
};

dclass DistributedGolfCourse : DistributedObject {
  setGolferIds(uint32[]) broadcast ram required;
  setCourseId(int8) broadcast ram required;
  setAvatarJoined() airecv clsend;
  setAvatarReadyCourse() airecv clsend;
  setAvatarReadyHole() airecv clsend;
  setAvatarExited() airecv clsend;
  setCurHoleIndex(int8) broadcast ram required;
  setCurHoleDoId(uint32) broadcast ram required;
  setDoneReward() airecv clsend;
  setReward(uint8[] [], int8[], uint8[] [], uint8[] [], uint8[] [], uint32, uint32/100, uint32/100, uint32/100, uint32/100) broadcast;
  setCourseReady(int8, int16[], int8) broadcast;
  setHoleStart(int16) broadcast;
  setCourseExit() broadcast;
  setCourseAbort(uint32) broadcast;
  setPlayHole() broadcast;
  avExited(uint32) broadcast;
  setScores(int16 []) broadcast;
  changeDrivePermission(uint32, int8) broadcast;
};

dclass DistributedVineGame : DistributedMinigame {
  reachedEndVine(int8) clsend airecv;
  setNewVine(uint32, int8, uint32/10000, int8) airecv clsend broadcast;
  setNewVineT(uint32, uint32/10000, int8) clsend broadcast;
  setJumpingFromVine(uint32, int8, int8, int32/100, int16/100, int16/100, int16) clsend broadcast;
  claimTreasure(uint32) airecv clsend;
  setTreasureGrabbed(uint32, uint32) broadcast;
  setScore(uint32, uint32) broadcast;
  allAtEndVine() broadcast;
  setFallingFromVine(uint32, int8, int8, int32/100, int16/100, int16/100, int16, int8) clsend broadcast;
  setFallingFromMidair(uint32, int8, int32/100, int16/100, int16/100, int16, int8) clsend broadcast;
  setVineSections(uint8[]) required broadcast ram;
};

dclass TTAvatarFriendsManager : AvatarFriendsManager {
};

dclass TTPlayerFriendsManager : PlayerFriendsManager {
};

dclass TTSpeedchatRelay : SpeedchatRelay {
};

dclass DistributedGolfKart : DistributedObject {
  setState(string, int16) broadcast ram;
  fillSlot0(uint32) broadcast ram;
  fillSlot1(uint32) broadcast ram;
  fillSlot2(uint32) broadcast ram;
  fillSlot3(uint32) broadcast ram;
  emptySlot0(uint32, int16) broadcast ram;
  emptySlot1(uint32, int16) broadcast ram;
  emptySlot2(uint32, int16) broadcast ram;
  emptySlot3(uint32, int16) broadcast ram;
  requestBoard() airecv clsend;
  rejectBoard(uint32);
  requestExit() airecv clsend;
  setMinigameZone(uint32, uint16);
  setGolfZone(uint32, uint16);
  setGolfCourse(int8) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setColor(int16, int16, int16) required broadcast ram;
};

dclass DistributedTimer : DistributedObject {
  setStartTime(int32) broadcast ram required;
};

dclass DistributedPicnicBasket : DistributedObject {
  setState(string, uint16, int16) broadcast ram;
  fillSlot0(uint32) broadcast ram;
  fillSlot1(uint32) broadcast ram;
  fillSlot2(uint32) broadcast ram;
  fillSlot3(uint32) broadcast ram;
  emptySlot0(uint32, int16) broadcast ram;
  emptySlot1(uint32, int16) broadcast ram;
  emptySlot2(uint32, int16) broadcast ram;
  emptySlot3(uint32, int16) broadcast ram;
  requestBoard(int16) airecv clsend;
  rejectBoard(uint32);
  requestExit() airecv clsend;
  doneExit() airecv clsend;
  setMinigameZone(uint32, uint16);
  setPicnicDone();
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setTableNumber(int16) required broadcast ram;
};

dclass DistributedGameTable : DistributedObject {
  requestJoin(uint8) airecv clsend;
  rejectJoin();
  requestExit() airecv clsend;
  fillSlot0(uint32) broadcast ram;
  fillSlot1(uint32) broadcast ram;
  fillSlot2(uint32) broadcast ram;
  fillSlot3(uint32) broadcast ram;
  fillSlot4(uint32) broadcast ram;
  fillSlot5(uint32) broadcast ram;
  emptySlot0(uint32, int16) broadcast ram;
  emptySlot1(uint32, int16) broadcast ram;
  emptySlot2(uint32, int16) broadcast ram;
  emptySlot3(uint32, int16) broadcast ram;
  emptySlot4(uint32, int16) broadcast ram;
  emptySlot5(uint32, int16) broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  announceWinner(uint32) broadcast;
};

dclass DistributedBossbotBoss : DistributedBossCog {
  setState(string) broadcast ram;
  setBattleDifficulty(uint8) broadcast ram;
  requestGetFood(int8, int8, uint32) airecv clsend;
  toonGotFood(uint32, int8, int8, uint32) broadcast;
  requestServeFood(int8, int8) airecv clsend;
  toonServeFood(uint32, int8, int8) broadcast;
  hitBoss(uint8) airecv clsend;
  hitToon(uint32) airecv clsend;
  ballHitBoss(uint8) airecv clsend;
  setBossDamage(uint16, uint8, int16) broadcast ram;
  setSpeedDamage(uint16, uint8, int16) broadcast ram;
  reachedTable(uint8) airecv clsend;
  hitTable(uint8) airecv clsend;
  awayFromTable(uint8) airecv clsend;
  toonGotHealed(uint32) broadcast;
  requestGetToonup(int8, int8, uint32) airecv clsend;
  toonGotToonup(uint32, int8, int8, uint32) broadcast;
};

dclass DistributedCogKart : DistributedElevatorExt {
  setCountryClubId(uint16) required broadcast ram;
  setPosHpr(int16/10, int16/10, int16/10, int16/10, int16/10, int16/10) required broadcast ram;
  setCountryClubInteriorZone(uint32);
  setCountryClubInteriorZoneForce(uint32);
};

dclass DistributedCountryClub : DistributedObject {
  setZoneId(uint32) required broadcast ram;
  setBlockedRooms(uint8[]) required broadcast ram;
  setCountryClubId(uint16) required broadcast ram;
  setLayoutIndex(uint16) required broadcast ram;
  setFloorNum(uint8) required broadcast ram;
  setRoomDoIds(uint32[]) broadcast ram;
  setCountryClubZone(uint32) broadcast ram;
  elevatorAlert(uint32) broadcast ram;
};

dclass DistributedCountryClubRoom : DistributedLevel {
  setCountryClubId(uint16) required broadcast ram;
  setRoomId(uint16) required broadcast ram;
  setRoomNum(uint8) required broadcast ram;
  setSuits(uint32[], uint32[]) broadcast ram;
  setBossConfronted(uint32) broadcast ram;
  setDefeated() broadcast ram;
  forceOuch(uint8) broadcast;
};

dclass DistributedMoleField : DistributedEntity {
  setGameStart(int16, uint8, uint16) broadcast;
  setClientTriggered() airecv clsend;
  whackedMole(int8, int16) airecv clsend;
  whackedBomb(int8, int16, int32) airecv clsend;
  updateMole(int8, int8) broadcast;
  reportToonHitByBomb(uint32, int8, int32) broadcast;
  setScore(int16) required broadcast ram;
  damageMe() airecv clsend;
  setPityWin() broadcast;
};

dclass DistributedCountryClubBattle : DistributedLevelBattle {
};

dclass DistributedClubElevator : DistributedElevatorFSM {
  setFloor(int8) broadcast ram;
  setLocked(uint16) required broadcast ram;
  setEntering(uint16) required broadcast ram;
  kickToonsOut() broadcast;
  setLatch(uint32) required broadcast ram;
};

dclass DistributedMaze : DistributedEntity {
  setRoomDoId(uint32) required broadcast ram;
  setGameStart(int16) broadcast;
  setClientTriggered() airecv clsend;
  setFinishedMaze() airecv clsend;
  setGameOver() broadcast;
  toonFinished(uint32, uint8, uint8) broadcast;
  damageMe() airecv clsend;
};

dclass DistributedBattleWaiters : DistributedBattleFinal {
};

dclass DistributedFoodBelt : DistributedObject {
  setBossCogId(uint32) required broadcast ram;
  setIndex(uint8) required broadcast ram;
  setState(char) broadcast ram;
};

dclass DistributedBanquetTable : DistributedObject {
  setIndex(uint8) required broadcast ram;
  setNumDiners(uint8) required broadcast ram;
  setBossCogId(uint32) required broadcast ram;
  setDinerInfo(uint8[], uint8[], uint8[], char[]) required broadcast ram;
  setState(char, uint32, int8) broadcast ram;
  setDinerStatus(uint8, uint8) broadcast;
  requestControl() airecv clsend;
  requestFree(int8) airecv clsend;
  setPitcherPos(uint8, uint16%360/100, int16) broadcast clsend;
  clearSmoothing(int8) broadcast clsend;
  firingWater(int32/100, int32/100, int32/100, int32/100, int32/100, int32/100) broadcast clsend;
  waterHitBoss(uint8) broadcast clsend;
};

dclass DistributedBattleDiners : DistributedBattleFinal {
};

dclass DistributedGolfSpot : DistributedObject {
  setIndex(uint8) required broadcast ram;
  setBossCogId(uint32) required broadcast ram;
  setState(char, uint32, int8) broadcast ram;
  setGoingToReward() broadcast ram;
  requestControl() airecv clsend;
  requestFree(int8) airecv clsend;
  setGolfSpotPos(uint8, uint16%360/100, int16) broadcast clsend;
  clearSmoothing(int8) broadcast clsend;
  setSwingInfo(uint8, int16/10, uint8) broadcast clsend;
};

struct TireInput {
  int32/100 force;
  int32/100 heading;
};

dclass DistributedIceGame : DistributedMinigame {
  setForceArrowInfo(uint32, int32/100, int32/100) broadcast clsend;
  setAvatarChoice(int32/100, int32/100) airecv clsend;
  endingPositions(Coord3 []) airecv clsend;
  reportScoringMovieDone() airecv clsend;
  claimTreasure(uint8) airecv clsend;
  claimPenalty(uint8) airecv clsend;
  setTireInputs(TireInput []) broadcast;
  setTimerStartTime(int16) broadcast;
  setFinalPositions(Coord3 []) broadcast;
  setMatchAndRound(int8, int8) broadcast;
  setScores(int8, int8, int16[]) broadcast;
  setNewState(string) broadcast;
  setTreasureGrabbed(uint32, uint32) broadcast;
  setPenaltyGrabbed(uint32, uint32) broadcast;
};

dclass DistributedCogThiefGame : DistributedMinigame {
  throwingPie(uint32, int32, int32/100, int32/100, int32/100, int32/100) clsend broadcast;
  hitBySuit(uint32, int32, int8, int32/100, int32/100, int32/100) clsend broadcast airecv;
  pieHitSuit(uint32, int32, int8, int32/100, int32/100, int32/100) clsend broadcast airecv;
  cogHitBarrel(int32, int8, int8, int32/100, int32/100, int32/100) clsend airecv;
  cogAtReturnPos(int32, int8, int8) clsend airecv;
  updateSuitGoal(int32, int32, int8, int8, int64, int32/100, int32/100, int32/100) broadcast;
  makeCogCarryBarrel(int32, int32, int8, int8, int32/100, int32/100, int32/100) broadcast;
  makeCogDropBarrel(int32, int32, int8, int8, int32/100, int32/100, int32/100) broadcast;
  markBarrelStolen(int32, int32, int8) broadcast;
};

struct twoDTreasureInfo {
  uint8 treasureIndex;
  uint8 treasureValue;
};

struct twoDSectionInfo {
  uint8 sectionIndex;
  uint8 enemyIndicesSelected[];
  twoDTreasureInfo treasureIndicesSelected[];
  uint8 spawnPointIndicesSelected[];
  uint8 stomperIndicesSelected[];
};

dclass DistributedTwoDGame : DistributedMinigame {
  showShootGun(uint32, int16) clsend broadcast;
  toonHitByEnemy(uint32, int16) clsend broadcast airecv;
  toonFellDown(uint32, int16) clsend broadcast airecv;
  toonSquished(uint32, int16) clsend broadcast airecv;
  toonVictory(uint32, int16) clsend broadcast airecv;
  claimTreasure(uint8, uint8) airecv clsend;
  claimEnemyShot(uint8, uint8) airecv clsend;
  reportDone() airecv clsend;
  setSectionsSelected(twoDSectionInfo []) required broadcast ram;
  setTreasureGrabbed(uint32, uint8, uint8) broadcast;
  setEnemyShot(uint32, uint8, uint8, uint32) broadcast;
  addVictoryScore(uint32, uint8) broadcast;
  setEveryoneDone() broadcast;
};

dclass DistributedChineseCheckers : DistributedNode {
  requestExit() clsend airecv;
  requestBegin() clsend airecv;
  requestMove(uint8 []) clsend airecv;
  requestTimer() clsend airecv;
  requestSeatPositions() clsend airecv;
  startBeginTimer(uint16, int16) broadcast ram;
  gameStart(uint8) broadcast;
  setTableDoId(uint32) required broadcast ram;
  setGameState(uint8 [], uint8 []) required broadcast ram;
  setTimer(int16) broadcast ram required;
  setTurnTimer(int16) broadcast ram required;
  sendTurn(uint8) broadcast ram;
  requestWin() clsend airecv;
  announceWin(uint32) broadcast;
  announceSeatPositions(uint8 []) broadcast;
};

dclass DistributedCheckers : DistributedNode {
  requestExit() clsend airecv;
  requestBegin() clsend airecv;
  requestTimer() clsend airecv;
  requestMove(uint8 []) clsend airecv;
  startBeginTimer(uint16, int16) broadcast ram;
  gameStart(uint8) broadcast;
  setTableDoId(uint32) required broadcast ram;
  setGameState(uint8 [], uint8 []) required broadcast ram;
  setTimer(int16) broadcast ram required;
  setTurnTimer(int16) broadcast ram required;
  sendTurn(uint8) broadcast ram;
  requestWin() clsend airecv;
  announceWin(uint32) broadcast;
  illegalMove() broadcast;
};

dclass DistributedFindFour : DistributedNode {
  requestExit() clsend airecv;
  requestBegin() clsend airecv;
  requestMove(uint8) clsend airecv;
  requestTimer() clsend airecv;
  requestWin(uint8 []) clsend airecv;
  startBeginTimer(uint16, int16) broadcast ram;
  setTableDoId(uint32) required broadcast ram;
  setGameState(uint8 [][], uint8, uint8, uint8) required broadcast ram;
  setTimer(int16) broadcast ram required;
  setTurnTimer(int16) broadcast ram required;
  gameStart(uint8) broadcast;
  sendTurn(uint8) broadcast ram;
  announceWin(uint32) broadcast;
  announceWinLocation(uint8, uint8, uint8, uint8) broadcast;
  announceWinnerPosition(uint8, uint8, uint8, uint8) broadcast;
  illegalMove() broadcast;
  tie() broadcast;
};

dclass DistributedMailManager : DistributedObject {
  sendSimpleMail(uint32, uint32, string);
  setNumMailItems(uint32, uint32) airecv;
};

struct PotentialToon {
  uint32 avNum;
  string avName;
  string avDNA;
  uint8 avPosition;
  uint8 aname;
  int16 hp;
  int16 maxHp;
  uint8[] hat;
  uint8[] glasses;
  uint8[] backpack;
  uint8[] shoes;
};

dclass ClientServicesManager : DistributedObjectGlobal {
  login(string cookie, char auth [0-256]) clsend;
  acceptLogin(uint32 timestamp);

  requestAvatars() clsend;
  setAvatars(PotentialToon[]);

  createAvatar(blob dna, uint8 index, uint8 uber, uint16[], uint8 pg) clsend;
  createAvatarResp(uint32 avId);

  setNameTyped(uint32 avId, string name) clsend;
  setNameTypedResp(uint32 avId, uint8 status);
  setNamePattern(uint32 avId, int16 p1, uint8 f1, int16 p2, uint8 f2, int16 p3, uint8 f3, int16 p4, uint8 f4) clsend;
  setNamePatternResp(uint32 avId, uint8 status);

  acknowledgeAvatarName(uint32 avId) clsend;
  acknowledgeAvatarNameResp();

  deleteAvatar(uint32 avId) clsend;

  chooseAvatar(uint32 avId) clsend;

  systemMessage(string message);
};

dclass AwardManager : DistributedObjectGlobal {
  giveAwardToToon(uint32, DoId, string, DoId, uint32, uint32);
};

dclass DistributedCpuInfoMgr : DistributedObjectGlobal {
  setCpuInfoToUd(uint32, uint32, string, string);
};

dclass DistributedSecurityMgr : DistributedObjectGlobal {
  requestAccountId(uint32, uint32, uint32);
  requestAccountIdResponse(uint32, uint32) airecv;
};

dclass NonRepeatableRandomSourceClient {
  getRandomSamplesReply(uint32, uint32 []) airecv;
};

dclass TTCodeRedemptionMgr : DistributedObject, NonRepeatableRandomSourceClient {
  giveAwardToToonResult(uint32, uint32);
  redeemCode(uint32, char [0-256]) airecv clsend;
  redeemCodeAiToUd(uint32, DoId, uint32, string, uint32);
  redeemCodeResultUdToAi(uint32, uint32, uint32, uint32, uint32) airecv;
  redeemCodeResult(uint32, uint32, uint32);
};

dclass NonRepeatableRandomSource : DistributedObject, NonRepeatableRandomSourceClient {
  getRandomSamples(DoId, string, uint32, uint32);
  randomSample(DoId, uint32);
  randomSampleAck() airecv;
};

dclass DistributedInGameNewsMgr : DistributedObjectGlobal {
  setLatestIssueStr(string) required broadcast ram;
  inGameNewsMgrAIStartingUp(uint32, uint32);
  newIssueUDtoAI(string) airecv;
};

dclass DistributedWhitelistMgr : DistributedObjectGlobal {
  updateWhitelist() broadcast;
  whitelistMgrAIStartingUp(uint32, uint32);
  newListUDtoAI() airecv;
};

struct Friend
{
uint32 doId;
string name;
blob dna;
uint32 petId;
};

dclass TTAFriendsManager : DistributedObjectGlobal {
  removeFriend(uint32) clsend;
  requestAvatarInfo(uint32[]) clsend;

  requestFriendsList() clsend;

  friendInfo(Friend);
  friendList(Friend []);

  friendOnline(uint32, uint8, uint8);
  friendOffline(uint32);

  goingOffline(uint32 avId);

  getAvatarDetails(uint32) clsend;
  getPetDetails(uint32) clsend;

  friendDetails(uint32, blob, uint16[], uint16, int16, int16, uint32, uint32, blob, blob, int8[]);
  petDetails(uint32, uint32, string, uint32, uint32, uint16/1000[], PetTrait[], int8[], uint32);

  routeTeleportQuery(uint32 toId) clsend;
  teleportQuery(uint32 fromId);

  teleportResponse(uint32 fromId, uint8 tpAvailable, uint32 defaultShard, uint32 hoodId, uint32 zoneId) clsend;
  setTeleportResponse(uint32 toId, uint8 tpAvailable, uint32 defaultShard, uint32 hoodId, uint32 zoneId);

  whisperSCTo(uint32 toId, uint16 msgIndex) clsend;
  setWhisperSCFrom(uint32 fromId, uint16 msgIndex);

  whisperSCCustomTo(uint32 toId, uint16 msgIndex) clsend;
  setWhisperSCCustomFrom(uint32 fromId, uint16 msgIndex);

  whisperSCEmoteTo(uint32 toId, uint16 emoteId) clsend;
  setWhisperSCEmoteFrom(uint32 fromId, uint16 emoteId);

  requestSecret() clsend;
  requestSecretResponse(int8 status, string secret);

  submitSecret(string(0-256) secret) clsend;
  submitSecretResponse(int8 status, int32 avId);

  sendTalkWhisper(uint32 toId, string message) clsend;
  receiveTalkWhisper(uint32 fromId, string message);

  battleSOS(uint32 toId) clsend;
  setBattleSOS(uint32 fromId);

  teleportGiveup(uint32 toId) clsend;
  setTeleportGiveup(uint32 fromId);

  whisperSCToontaskTo(uint32, uint32, uint32, uint32, uint8) clsend;
  setWhisperSCToontaskFrom(uint32, uint32, uint32, uint32, uint8);

  sleepAutoReply(uint32 toId) clsend;
  setSleepAutoReply(uint32 fromId);
};


dclass DistributedPhaseEventMgr : DistributedObject {
  setNumPhases(uint8) required broadcast ram;
  setDates(datetime []) broadcast required;
  setCurPhase(int8) required broadcast ram;
  setIsRunning(bool) required broadcast ram;
};

dclass DistributedHydrantZeroMgr : DistributedPhaseEventMgr {
};

dclass DistributedMailboxZeroMgr : DistributedPhaseEventMgr {
};

dclass DistributedTrashcanZeroMgr : DistributedPhaseEventMgr {
};

dclass DistributedSillyMeterMgr : DistributedPhaseEventMgr {
};

dclass DistributedEvent : DistributedObject {
  start() broadcast ram;
  setState(string, int32) broadcast ram;
};

dclass DistributedBetaEvent : DistributedEvent {
};

dclass DistributedBetaEventTTC : DistributedEvent {
};

dclass DistributedWeatherCycle : DistributedObject {
  setState(string) required broadcast ram;
  setDuration(int32) required broadcast ram;
};

dclass DistributedWeatherStorm : DistributedObject {
  start() broadcast;
  stop() broadcast;
  setStormType(int8) broadcast ram;
  setDuration(int32) broadcast ram;
};

struct Member {
  uint32 doId;
}

dclass DistributedToonClub : DistributedObjectGlobal {
  requestStats() clsend;
  addMember(uint32) clsend;
  removeMember(uint32);
  setMembers(Member []);
};

dclass DistributedWeatherMGR : DistributedObject {
  start() broadcast ram;
  setState(string, int32) broadcast ram;
};

dclass DistributedDayTimeManager : DistributedWeatherMGR {
  update(int8) broadcast ram;
};

dclass DistributedRainManager : DistributedWeatherMGR {
  spawnLightning(int16, int16) broadcast ram;
};

"""

######## TURN ME OFF IN PRODUCTION ########
dcStream = StringStream(dcString)
def getDcStream():
    return dcStream

import toontown.toonbase.ClientStart
