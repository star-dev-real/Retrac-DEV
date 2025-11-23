import json
from datetime import datetime
import hashlib

from mitmproxy import http

DEFAULT_GAME = """; [/Script/Engine.AssetManagerSettings]
; +PrimaryAssetTypesToScan=(PrimaryAssetType="AthenaCharacter",AssetBaseClass=/Script/FortniteGame.AthenaCharacterItemDefinition,bHasBlueprintClasses=False,bIsEditorOnly=False,Directories=((Path="/Game/Athena/Items/Cosmetics/Characters"),(Path="/Game/Retrac/Items/Cosmetics/Characters")),SpecificAssets=,Rules=(Priority=20,bApplyRecursively=True,ChunkId=1,CookRule=AlwaysCook)

[/Script/FortniteGame.FortGlobals]
bAllowLogout=false
bEnableCreativeMode=false
bTwitchEnabled=false
bEnableAccountLinkingUIURLButton=true
bUploadAthenaStats=true
bUploadAthenaStatsV2=true

[/Script/FortniteGame.FortChatManager]
bShouldRequestGeneralChatRooms=false
bShouldJoinGlobalChat=false
bShouldJoinFounderChat=false
bIsAthenaGlobalChatEnabled=false

[/Script/FortniteGame.FortOnlineAccount]
bEnableEulaCheck=false
bShouldCheckIfPlatformAllowed=false
!WebCreateEpicAccountUrl=ClearArray

[/Script/FortniteGame.FortTextHotfixConfig]
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="38E78EA54967AD3E123D289F41C0CFB7", NativeString="Congratulations on your excellent performance in a recent tournament event!", LocalizedStrings=(("en","Congratulations on your excellent performance in arena!")))
# +TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="A4EB1D3F49DBBC0B9EE9DC8D3F6A6196", NativeString="{0} {0}|plural(one=Elimination,other=Eliminations)", LocalizedStrings=(("en","{0}|plural(one=Each Elimination,other=Every {0} Eliminations)")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="52A8624F42BCFA3B45E7D182EA2308D6", NativeString="{0}|plural(one=Each Elimination,other=Every {0} Eliminations)", LocalizedStrings=(("en","{0}|plural(one={0} Elimination,other={0} Eliminations)")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="EEB756A54C4C7AE9C7D837B11E9CD8FB", NativeString="Mineluke", LocalizedStrings=(("en","Wii Mii")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="AF30A19046D3EBD39404D3A56A62C832", NativeString="Mineluke Shuffle", LocalizedStrings=(("en","Wii Shuffle")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="FEA927E149548751BF841698641C2BB8", NativeString="Peace returns to those that wish for it. discord.gg/cosmos", LocalizedStrings=(("en","Peace returns to those that wish for it.")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="56198E2E48298607D0A3AC9CE71D5835", NativeString="Directly exported from my WII. Made by boredcrow", LocalizedStrings=(("en","Directly exported from my Wii.")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="ABA392084B7466BE7D610FAAD02167AF", NativeString=" Silver Surfer's Board", LocalizedStrings=(("en"," Surfer Silfer")))

#+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="AthenaSeasonItemDefinitionInternal", Key="ChapterTextFormat", NativeString="Chapter {0}", LocalizedStrings=(("ar","Chapter {0} Season 4"),("en","Chapter {0} Season 4"),("de","Chapter {0} Season 4"),("es","Chapter {0} Season 4"),("es-419","Chapter {0} Season 4"),("fr","Chapter {0} Season 4"),("it","Chapter {0} Season 4"),("ja","Chapter {0} Season 4"),("ko","Chapter {0} Season 4"),("pl","Chapter {0} Season 4"),("pt-BR","Chapter {0} Season 4"),("ru","Chapter {0} Season 4"),("tr","Chapter {0} Season 4"),("zh-CN","Chapter {0} Season 4"),("zh-Hant","Chapter {0} Season 4")))
#+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="AthenaSeasonItemDefinitionInternal", Key="SeasonTextFormat", NativeString="Season {0}", LocalizedStrings=(("ar","Freetrac"),("en","Freetrac"),("de","Freetrac"),("es","Freetrac"),("es-419","Freetrac"),("fr","Freetrac"),("it","Freetrac"),("ja","Freetrac"),("ko","Freetrac"),("pl","Freetrac"),("pt-BR","Freetrac"),("ru","Freetrac"),("tr","Freetrac"),("zh-CN","Freetrac"),("zh-Hant","Freetrac")))

+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="04DF040F4FBD6CE4F70F6F9B04171DD8", NativeString="Tournament", LocalizedStrings=(("en","Lategame Arena")))


# 1v1
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="240C909D47B5EF6C3406F2A6ED429696", NativeString="Customize", LocalizedStrings=(("ar","Reset builds"),("en","Reset builds"),("de","Reset builds"),("es","Reset builds"),("es-419","Reset builds"),("fr","Reset builds"),("it","Reset builds"),("ja","Reset builds"),("ko","Reset builds"),("pl","Reset builds"),("pt-BR","Reset builds"),("ru","Reset builds"),("tr","Reset builds"),("zh-CN","Reset builds"),("zh-Hant","Reset builds")))

# Scrims
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="C37042DB4C4F5AE15CB9999C67869AB1", NativeString="Siphon", LocalizedStrings=(("ar","Freetrac Scrims"),("en","Freetrac Scrims"),("de","Freetrac Scrims"),("es","Freetrac Scrims"),("es-419","Freetrac Scrims"),("fr","Freetrac Scrims"),("it","Freetrac Scrims"),("ja","Freetrac Scrims"),("ko","Freetrac Scrims"),("pl","Freetrac Scrims"),("pt-BR","Freetrac Scrims"),("ru","Freetrac Scrims"),("tr","Freetrac Scrims"),("zh-CN","Freetrac Scrims"),("zh-Hant","Freetrac Scrims")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="EB35C2D1457494740BA86FA27F922402", NativeString="All healing items have been removed in this mode. The only way to gain health or shields is to eliminate your opponents!", LocalizedStrings=(("ar","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("en","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("de","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("es","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("es-419","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("fr","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("it","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("ja","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("ko","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("pl","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("pt-BR","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("ru","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("tr","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("zh-CN","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle."),("zh-Hant","You can fight until 80 players remain. After that, no fighting until 4th zone or Storm Surge warning. Play smart, stay patient, and survive 'til it's time to battle.")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="0C6895884EFF128AAD75DFA9E059AE63", NativeString="No Healing Items", LocalizedStrings=(("ar","No griefers!"),("en","No griefers!"),("de","No griefers!"),("es","No griefers!"),("es-419","No griefers!"),("fr","No griefers!"),("it","No griefers!"),("ja","No griefers!"),("ko","No griefers!"),("pl","No griefers!"),("pt-BR","No griefers!"),("ru","No griefers!"),("tr","No griefers!"),("zh-CN","No griefers!"),("zh-Hant","No griefers!")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="85CA91444D4C2AC56CBDC7ABB0D84996", NativeString="Don't bother searching for bandages or shield pots - eliminations are the only way to gain health.", LocalizedStrings=(("en","Storm circles move a lot faster and start very small, make sure to keep moving!")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="63B94DA0479A3B1687CDA589E5CA350D", NativeString="Guns... lots of Guns", LocalizedStrings=(("en","Random Loadouts")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="BB812BFA4276FF5A95668A893B41FDC6", NativeString="No healing items means lots of room in your inventory for weapons. " LocalizedStrings=(("en","Randomised loadouts mean you'll have to adapt to whatever you're given!")))
+TextReplacements=(Category=Game, bIsMinimalPatch=True, Namespace="", Key="2D533B2C4A9C3132AE558ABD58FA185B", NativeString="Tournament" LocalizedStrings=(("en","Lategame")))

[/Script/FortniteGame.FortGameInstance]
!FrontEndPlaylistData=ClearArray
+FrontEndPlaylistData=(PlaylistName=Playlist_DefaultSolo, PlaylistAccess=(bEnabled=false, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=False, CategoryIndex=0, bDisplayAsLimitedTime=False, DisplayPriority=0))
+FrontEndPlaylistData=(PlaylistName=Playlist_DefaultDuo, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=False, CategoryIndex=0, bDisplayAsLimitedTime=False, DisplayPriority=1))
+FrontEndPlaylistData=(PlaylistName=Playlist_DefaultSquad, PlaylistAccess=(bEnabled=false, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=False, CategoryIndex=0, bDisplayAsLimitedTime=False, DisplayPriority=2))

#+FrontEndPlaylistData=(PlaylistName=Playlist_Lite_Solo, PlaylistAccess=(bEnabled=false, bIsDefaultPlaylist=True, bVisibleWhenDisabled=True, bDisplayAsNew=False, CategoryIndex=0, bDisplayAsLimitedTime=False, DisplayPriority=3))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Retrac_Turtle, PlaylistAccess=(bEnabled=false, bIsDefaultPlaylist=True, bVisibleWhenDisabled=True, bDisplayAsNew=False, CategoryIndex=1, bDisplayAsLimitedTime=False, DisplayPriority=3))
# +FrontEndPlaylistData=(PlaylistName=Playlist_Gungame_Reverse, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=True, CategoryIndex=1, bDisplayAsLimitedTime=False, DisplayPriority=2))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Low_Squads, PlaylistAccess=(bEnabled=False, bIsDefaultPlaylist=False, bVisibleWhenDisabled=False, bDisplayAsNew=True, CategoryIndex=0, bDisplayAsLimitedTime=True, DisplayPriority=3))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Vamp_Trio, PlaylistAccess=(bEnabled=false, bIsDefaultPlaylist=True, bVisibleWhenDisabled=False, bDisplayAsNew=False, CategoryIndex=1, bDisplayAsLimitedTime=True, DisplayPriority=0))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Vamp_Solo, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=True, bVisibleWhenDisabled=False, bDisplayAsNew=False, CategoryIndex=1, bDisplayAsLimitedTime=True, DisplayPriority=0))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Vamp_Duos, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=True, bVisibleWhenDisabled=False, bDisplayAsNew=False, CategoryIndex=1, bDisplayAsLimitedTime=True, DisplayPriority=0))
#+FrontEndPlaylistData=(PlaylistName=Playlist_Low_Squads, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=True, bVisibleWhenDisabled=False, bDisplayAsNew=False, CategoryIndex=1, bDisplayAsLimitedTime=True, DisplayPriority=1))
# +FrontEndPlaylistData=(PlaylistName=Playlist_BattleLab, PlaylistAccess=(bEnabled=False, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=True, CategoryIndex=1, bDisplayAsLimitedTime=Flase, DisplayPriority=1))
+FrontEndPlaylistData=(PlaylistName=Playlist_Vamp_Solo, PlaylistAccess=(bEnabled=True, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=True, CategoryIndex=1, bDisplayAsLimitedTime=False, DisplayPriority=1))
+FrontEndPlaylistData=(PlaylistName=Playlist_Gungame_Reverse, PlaylistAccess=(bEnabled=False, bIsDefaultPlaylist=False, bVisibleWhenDisabled=True, bDisplayAsNew=True, CategoryIndex=1, bDisplayAsLimitedTime=Flase, DisplayPriority=1))

[AssetHotfix]
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.AssaultAuto.C0;ItemDefinition;WID_Assault_Stark_Athena_VR_Ore_T03

# overwrite shotgun with pumpkin launcher
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.01;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_VR_Ore_T03
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.02;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_SR_Ore_T03
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.03;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_SR_Ore_T03
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.04;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_SR_Ore_T03
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.05;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_SR_Ore_T03
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.016;ItemDefinition;/Game/Athena/Items/Weapons/Seasonal/WID_Launcher_Pumpkin_Athena_SR_Ore_T03

# troll lootpool
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.01;ItemDefinition;/Mantis/Items/UncleBrolly/WID_UncleBrolly.uasset
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.02;ItemDefinition;/Game/Items/Weapons/Ranged/Assault/NeonGlow_Assault/WID_Assault_NeonGlow_SR_Ore_T01
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.03;ItemDefinition;/Game/Items/Weapons/Ranged/Assault/NeonGlow_Assault/WID_Assault_NeonGlow_SR_Ore_T01
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.04;ItemDefinition;/Game/Items/Weapons/Ranged/Assault/NeonGlow_Assault/WID_Assault_NeonGlow_SR_Ore_T01
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.05;ItemDefinition;/Game/Items/Weapons/Ranged/Assault/NeonGlow_Assault/WID_Assault_NeonGlow_SR_Ore_T01
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaLoot.Weapon.Shotgun.016;ItemDefinition;/Game/Items/Weapons/Ranged/Assault/NeonGlow_Assault/WID_Assault_NeonGlow_SR_Ore_T01

#witch broom
# +DataTable=/Game/Items/DataTables/AthenaLootPackages_Client;RowUpdate;WorldList.AthenaHighConsumables.70;Weight;0.35

[/Script/FortniteGame.FortGameModeAthena]
+HotfixKillVolumes=(Map="Apollo_Terrain",Center=(X=-50250.000000,Y=-41680.000000,Z=-7380.000000),Extent=(X=78814.242188,Y=46661.640625,Z=1143.801636),Rotation=(Pitch=0.000000,Yaw=0.000000,Roll=0.000000))

[/Script/FortniteGame.FortPlayerController]
bServerSideHitMarkers=false

[Playlist_ShowdownAlt_Trios FortPlaylistAthena]
bAllowSquadFillOption=true

[/Game/Athena/Playlists/Vamp/Playlist_Vamp_Duos.Playlist_Vamp_Duos]
bAllowSquadFillOption=true

[/Script/FortniteGame.FortGameSessionDedicatedAthena]
bEnableMMSBackfill=true

[/Script/FortniteGame.FortPlayerController]
bClientSideEditPrediction=true

[VoiceChatManager]
bEnabled=true
bEnableOnLoadingScreen=false
bObtainJoinTokenFromPartyService=true
bAllowStateTransitionOnLoadingScreen=false
MaxRetries=5
RetryTimeJitter=1.0
RetryTimeBase=3.0
RetryTimeMultiplier=1.0
MaxRetryDelay=240.0
RequestJoinTokenTimeout=10.0
JoinChannelTimeout=120.0
VoiceChatImplementation=EOSVoiceChat
NetworkTypePollingDelay=0.0
PlayJoinSoundRecentLeaverDelaySeconds=30.0
DefaultInputVolume=1.0
DefaultOutputVolume=1.0
JoinTimeoutRecoveryMethod=Reinitialize
JoinErrorWorkaroundMethod=ResetConnection
NetworkChangeRecoveryMethod=ResetConnection
bEnableBluetoothMicrophone=false
VideoPreferredFramerate=0
bEnableEOSReservedAudioStreams=true

[VoiceChat.EOS]
bEnabled=true

[EOSSDK]
ProductName=VoicePlugin
ProductVersion=0.1
ProductId=36a9fc57194b4e3a8180f24e16b9db00
SandboxId=2b25f254556a47ab9c4c3734835323b7
DeploymentId=26c771c9b33a40d480222895a410d2c9
ClientId=xyza78918ZtWVAmjItRDbVQDUaNXpcIa
ClientSecret=NieVvGSZaNsTnRXkQr/oDylHg8joaU9Z7gKKsAZyEKY


[/Script/FortniteGame.FortPlayerPawnAthena]
ReviveFromDBNOTime=5.0"""

default_runtime = """[/Script/FortniteGame.FortRuntimeOptions]
!DisabledFrontendNavigationTabs=ClearArray
+DisabledFrontendNavigationTabs=(TabName="AthenaChallenges",TabState=EFortRuntimeOptionTabState::Hidden)
+DisabledFrontendNavigationTabs=(TabName="Showdown",TabState=EFortRuntimeOptionTabState::Hidden)
;+DisabledFrontendNavigationTabs=(TabName="AthenaStore",TabState=EFortRuntimeOptionTabState::Hidden)

bForceBRMode=True
bSkipSubgameSelect=True
bLoadDirectlyIntoLobby=True
bEnableInGameMatchmaking=True
MinimumAccountLevelForTournamentPlay=1
bSkipTrailerMovie=true
bAlwaysPlayTrailerMovie=false

bEnableGlobalChat=true
bDisableGifting=false
bDisableGiftingPC=false
bDisableGiftingPS4=false
bDiableGiftingXB=false
MaxPartySizeAthena=16
MaxPartySizeCampaign=16
MaxSquadSize=16
bAllowMimicingEmotes=true
+ExperimentalCohortPercent=(CohortPercent=100,ExperimentNum=20)

; ARENA POINTS FETCH AFTER LEAVING GAME
ShowdownTournamentCacheExpirationHours=1
TournamentRefreshPlayerMaxRateSeconds=1
TournamentRefreshEventsMaxRateSeconds=1
TournamentRefreshPayoutMaxRateSeconds=1

; 14.30 NEW STORE
bShowStoreBanner=true
bEnableCatabaDynamicBackground=true
NewMtxStoreCohortSampleSet=100
+ExperimentalCohortPercent=(CohortPercent=100,ExperimentNum=14)
+ExperimentalCohortPercent=(CohortPercent=100,ExperimentNum=15)

[/Script/FortniteGame.FortPlayerController]
bServerSideHitMarkers=false
bClientSideEditPrediction=true

[/Script/FortniteGame.FortPlayerPawnAthena]
ReviveFromDBNOTime=5.0"""

default_engine = """[XMPP]
bEnableWebsockets=true

[OnlineSubsystem]
bHasVoiceEnabled=true

[ConsoleVariables]
Store.EnableCatabaScreen=1
Store.EnableCatabaHighlights=1

[ConsoleVariables]
n.VerifyPeer=0
FortMatchmakingV2.ContentBeaconFailureCancelsMatchmaking=0
Fort.ShutdownWhenContentBeaconFails=0
FortMatchmakingV2.EnableContentBeacon=0

[Core.Log]
LogPurchaseFlow=verbose
LogDiscordRPC=verbose
LogVoiceChatManager=All

[/Script/Qos.QosRegionManager]
NumTestsPerRegion=5
PingTimeout=3.0
!RegionDefinitions=ClearArray
+RegionDefinitions=(DisplayName=NSLOCTEXT("MMRegion", "Europe (France, Gravelines)", "Europe (France, Gravelines)"), RegionId="EU", bEnabled=true, bVisible=true, bAutoAssignable=true)
+RegionDefinitions=(DisplayName=NSLOCTEXT("MMRegion", "North America East (Virginia)", "NA East (Virginia)"), RegionId="NA", bEnabled=true, bVisible=true, bAutoAssignable=true)
+RegionDefinitions=(DisplayName=NSLOCTEXT("MMRegion", "North America West (Los Angeles)", "NA West (Los Angeles)"), RegionId="NAW", bEnabled=true, bVisible=true, bAutoAssignable=true)
+RegionDefinitions=(DisplayName=NSLOCTEXT("MMRegion", "Middle East (Dubai)", "Middle East (Dubai)"), RegionId="ME", bEnabled=true, bVisible=true, bAutoAssignable=true)
+RegionDefinitions=(DisplayName=NSLOCTEXT("MMRegion", "Oceania (Sydney)", "Oceania (Sydney)"), RegionId="OCE", bEnabled=true, bVisible=true, bAutoAssignable=true)

!DatacenterDefinitions=ClearArray
+DatacenterDefinitions=(Id="EU", RegionId="EU", bEnabled=true, Servers[0]=(Address="51.161.222.52", Port=7777))
+DatacenterDefinitions=(Id="NA", RegionId="NA", bEnabled=true, Servers[0]=(Address="51.161.222.52", Port=7777))
+DatacenterDefinitions=(Id="NAW", RegionId="NAW", bEnabled=true, Servers[0]=(Address="51.161.222.52", Port=7777))
+DatacenterDefinitions=(Id="ME", RegionId="ME", bEnabled=true, Servers[0]=(Address="51.161.222.52", Port=7777))
+DatacenterDefinitions=(Id="OCE", RegionId="OCE", bEnabled=true, Servers[0]=(Address="51.161.222.52", Port=7777))

!Datacenters=ClearArray
+Datacenters=(DisplayName=NSLOCTEXT("MMRegion", "EU", "EU"), RegionId="EU", bEnabled=true, bVisible=true, bBeta=false, Servers[0]=(Address="51.161.222.52", Port=7777))
+Datacenters=(DisplayName=NSLOCTEXT("MMRegion", "NA", "NA"), RegionId="NA", bEnabled=true, bVisible=true, bBeta=false, Servers[0]=(Address="51.161.222.52", Port=7777))
+Datacenters=(DisplayName=NSLOCTEXT("MMRegion", "NAW", "NAW"), RegionId="NAW", bEnabled=true, bVisible=true, bBeta=false, Servers[0]=(Address="51.161.222.52", Port=7777))
+Datacenters=(DisplayName=NSLOCTEXT("MMRegion", "ME", "ME"), RegionId="ME", bEnabled=true, bVisible=true, bBeta=false, Servers[0]=(Address="51.161.222.52", Port=7777))
+Datacenters=(DisplayName=NSLOCTEXT("MMRegion", "OCE", "OCE"), RegionId="OCE", bEnabled=true, bVisible=true, bBeta=false, Servers[0]=(Address="51.161.222.52", Port=7777))

[OnlineSubsystemMcp.Xmpp]
bUseSSL=false
ServerAddr="tcp.retrac.site"
ServerPort=1111

[OnlineSubsystemMcp.Xmpp Prod]
bUseSSL=false
Protocol=ws
ServerAddr="tcp.retrac.site"
ServerPort=1111

[/Script/FortniteGame.FortPlayerController]
bClientSideEditPrediction=true

[/Script/FortniteGame.FortPlayerController]
bServerSideHitMarkers=false

[OnlineSubsystem]
bHasVoiceEnabled=true

[Voice]
bEnabled=true

[VoiceChatManager]
bEnabled=true
bEnableOnLoadingScreen=false
bObtainJoinTokenFromPartyService=true
bAllowStateTransitionOnLoadingScreen=false
MaxRetries=5
RetryTimeJitter=1.0
RetryTimeBase=3.0
RetryTimeMultiplier=1.0
MaxRetryDelay=240.0
RequestJoinTokenTimeout=10.0
JoinChannelTimeout=120.0
VoiceChatImplementation=EOSVoiceChat
NetworkTypePollingDelay=0.0
PlayJoinSoundRecentLeaverDelaySeconds=30.0
DefaultInputVolume=1.0
DefaultOutputVolume=1.0
JoinTimeoutRecoveryMethod=Reinitialize
JoinErrorWorkaroundMethod=ResetConnection
NetworkChangeRecoveryMethod=ResetConnection
bEnableBluetoothMicrophone=false
VideoPreferredFramerate=0
bEnableEOSReservedAudioStreams=true

[VoiceChat.EOS]
bEnabled=true
ProductId=54acdc11395f4fc4b3b4e72f9d106f30
SandboxId=c4952ee30d284d739769a50c9fe84efd
DeploymentId=a9f423cf42044a6d96610e1e349b81d4
ClientId=xyza78917RAgTsBPVeQwApf2jnhRwqXP
ClientSecret=Uali1cDwfbKRXleNX2Kcaglm61fjBRWoPXSbIeFlI0M

[EOSSDK]
ProductName=VoicePlugin
ProductVersion=0.1
ProductId=54acdc11395f4fc4b3b4e72f9d106f30
SandboxId=c4952ee30d284d739769a50c9fe84efd
DeploymentId=a9f423cf42044a6d96610e1e349b81d4
ClientId=xyza78917RAgTsBPVeQwApf2jnhRwqXP
ClientSecret=Uali1cDwfbKRXleNX2Kcaglm61fjBRWoPXSbIeFlI0M

[/Script/FortniteGame.FortPlayerPawnAthena]
ReviveFromDBNOTime=5.0"""

def compute_hashes(data: str):
    encoded = data.encode("utf-8")
    return hashlib.sha1(encoded).hexdigest(), hashlib.sha256(encoded).hexdigest()

class DefaultGame:
    def request(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url

        if "/fortnite/api/cloudstorage/system" in url and not url.endswith("/DefaultGame.ini"):
            flow.response = http.Response.make(
                200,
                b"",
                {"Content-Type": "text/plain"}
            )

        elif url.endswith("/fortnite/api/cloudstorage/system/DefaultGame.ini"):
            flow.response = http.Response.make(
                200,
                b"",
                {"Content-Type": "text/plain"}
            )

    def response(self, flow: http.HTTPFlow):
        url = flow.request.pretty_url

        if "/fortnite/api/cloudstorage/system" in url and not url.endswith("/DefaultGame.ini"):
            sha1, sha256 = compute_hashes(DEFAULT_GAME)
            metadata = [{
                "uniqueFilename": "DefaultGame.ini",
                "filename": "DefaultGame.ini",
                "hash": sha1,
                "hash256": sha256,
                "length": len(DEFAULT_GAME.encode("utf-8")),
                "contentType": "text/plain",
                "uploaded": datetime.utcnow().isoformat() + "Z",
                "storageType": "S3",
                "doNotCache": True
            }]
            flow.response = http.Response.make(
                200,
                json.dumps(metadata),
                {"Content-Type": "application/json"}
            )

        elif url.endswith("/fortnite/api/cloudstorage/system/DefaultGame.ini"):
            flow.response = http.Response.make(
                200,
                DEFAULT_GAME,
                {"Content-Type": "text/plain"}
            )

        elif url.endswith("/fortnite/api/cloudstorage/system/DefaultEngine.ini"):
            flow.response = http.Response.make(
                200,
                default_engine,
                {"Content-Type": "text/plain"}
            )